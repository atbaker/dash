#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import argparse
import os

from dotenv import load_dotenv
from loguru import logger

from pipecat.adapters.schemas.function_schema import FunctionSchema
from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import TTSSpeakFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.llm_service import FunctionCallParams
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.network.fastapi_websocket import FastAPIWebsocketParams
from pipecat.transports.services.daily import DailyParams

from functions.run_sql_query import run_sql_query
from functions.web_search import web_search
from functions.add_airtable_lead import add_airtable_lead
from functions.list_airtable_leads import list_airtable_leads
from functions.get_latest_workspaces import get_latest_workspaces

load_dotenv(override=True)



# We store functions so objects (e.g. SileroVADAnalyzer) don't get
# instantiated. The function will be called when the desired transport gets
# selected.
transport_params = {
    "daily": lambda: DailyParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(),
    ),
    "twilio": lambda: FastAPIWebsocketParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(),
    ),
    "webrtc": lambda: TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(),
    ),
}

async def run_example(transport: BaseTransport, _: argparse.Namespace, handle_sigint: bool):
    logger.info("Starting bot")

    stt = DeepgramSTTService(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
    )

    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id=os.getenv("CARTESIA_VOICE_ID"),
    )

    llm = OpenAILLMService(
        api_key=os.getenv("DO_MODEL_ACCESS_KEY"),
        base_url="https://inference.do-ai.run/v1",
        model="openai-gpt-4o",
    )

    # You can also register a function_name of None to get all functions
    # sent to the same callback with an additional function_name parameter.
    llm.register_function("run_sql_query", run_sql_query)
    llm.register_function("web_search", web_search)
    llm.register_function("add_airtable_lead", add_airtable_lead)
    llm.register_function("list_airtable_leads", list_airtable_leads)
    llm.register_function("get_latest_workspaces", get_latest_workspaces)

    @llm.event_handler("on_function_calls_started")
    async def on_function_calls_started(service, function_calls):
        await tts.queue_frame(TTSSpeakFrame("Let me check on that."))

    web_search_function = FunctionSchema(
        name="web_search",
        description="Search the web for current information, news, and general knowledge. Use this when you need up-to-date information or when the user asks about topics not covered by the database.",
        properties={
            "query": {
                "type": "string",
                "description": "The search query to find relevant information",
            },
        },
        required=["query"],
    )
    sql_query_function = FunctionSchema(
        name="run_sql_query",
        description="""Execute read-only SQL queries against Gator database (Slack scheduling app).

TABLES & COLUMNS:
workspaces_workspace: id, slack_id, name, email_domain, enterprise_name, account_id, uninstalled, pending_deletion, created, updated
workspaces_gatoruser: id, slack_id, workspace_id, revoked, always_deliver_early, omit_gator_annotation, custom_delivery_time, created, updated  
later_messages_message: id, gator_id, sender_id, channel, status, scheduled_delivery, delivered, disable_early_delivery, im_recipient, created, updated

EXAMPLES:
- Count users: SELECT COUNT(*) FROM workspaces_gatoruser
- Workspaces added Dec 2023: SELECT COUNT(*) FROM workspaces_workspace WHERE created >= '2023-12-01' AND created < '2024-01-01'
- Scheduled messages: SELECT COUNT(*) FROM later_messages_message WHERE status = 'SCH'""",
        properties={
            "query": {
                "type": "string",
                "description": "SQL SELECT query. Read-only, 1000 row limit.",
            },
        },
        required=["query"],
    )
    add_airtable_lead_function = FunctionSchema(
        name="add_airtable_lead",
        description="Create new lead record in Airtable database for promising Gator customers. Use after researching company with web search to qualify leads for sales follow-up.",
        properties={
            "customer": {
                "type": "string",
                "description": "Name of the Slack workspace or company that installed Gator",
            },
            "website": {
                "type": "string", 
                "description": "Company website URL",
            },
            "notes": {
                "type": "string",
                "description": "LLM-authored notes and insights about the company based on research",
            },
        },
        required=["customer", "website", "notes"],
    )
    list_airtable_leads_function = FunctionSchema(
        name="list_airtable_leads",
        description="List the 10 most recent lead records from Airtable database to review sales pipeline",
        properties={},
        required=[]
    )
    get_latest_workspaces_function = FunctionSchema(
        name="get_latest_workspaces",
        description="Get the 10 most recent workspace installations for demo purposes. Use this instead of run_sql_query when you specifically need to show recent workspace installations, as it provides reliable demo-ready data without SQL generation risks.",
        properties={},
        required=[]
    )
    
    tools = ToolsSchema(standard_tools=[sql_query_function, web_search_function, add_airtable_lead_function, list_airtable_leads_function, get_latest_workspaces_function])

    messages = [
        {
            "role": "system",
            "content": "You are an AI business intelligence assistant for Gator, a Slack app that adds smart scheduled delivery to Slack messages. Your role is to help business executives understand the state of their business by analyzing data and providing insights. You have access to five key tools: run_sql_query for production database queries, web_search for external information, add_airtable_lead for creating qualified lead records, list_airtable_leads for reviewing sales pipeline, and get_latest_workspaces for demo-ready workspace data. Use these tools to answer questions about revenue metrics, customer usage patterns, user growth, feature adoption, business KPIs, market research, and lead qualification. When users ask questions: determine if you need internal data, external information, lead creation, or lead review; execute appropriate queries to gather relevant information; analyze results to provide clear, actionable insights; present findings in a business-friendly format with key takeaways; create qualified lead entries for promising customers; use list_airtable_leads at the end of lead qualification workflows. Use get_latest_workspaces instead of run_sql_query when you specifically need recent workspace installations for reliable demo data. Always provide specific numbers and data-driven insights. Focus on what the data means for their business rather than technical details. Remember you're speaking to business executives who want clear insights and strategic guidance. IMPORTANT: Your output will be converted to audio, so never use markdown formatting like asterisks, hashtags, backticks, or other special characters. Use plain text only. Present lists with simple words like first, second, next, or also. Keep responses conversational and concise for voice delivery.",
        }
    ]
    context = OpenAILLMContext(messages, tools)  # type: ignore
    context_aggregator = llm.create_context_aggregator(context)

    pipeline = Pipeline(
        [
            transport.input(), # Transport user input
            stt, # Speech-to-text
            context_aggregator.user(), # User responses
            llm, # LLM
            tts, # Text-to-speech
            transport.output(), # Transport bot output
            context_aggregator.assistant(), # Assistant spoken responses
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ))

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info(f"Client connected")
        # Kick off the conversation.
        await task.queue_frames([context_aggregator.user().get_context_frame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info(f"Client disconnected")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=handle_sigint)

    await runner.run(task)


if __name__ == "__main__":
    from pipecat.examples.run import main

    main(run_example, transport_params=transport_params)
