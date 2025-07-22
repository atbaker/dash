"""
Slack bot integration for DASH AI assistant.
Handles Slack events and conversations with DigitalOcean Agent.
"""
import re
from typing import List, Dict, Any, Optional
from slack_sdk import WebClient
from openai import OpenAI
from chat_service import get_chat_response
from markdown_to_mrkdwn import SlackMarkdownConverter


class SlackBot:
    def __init__(self, slack_token: str, openai_client: OpenAI):
        self.slack_client = WebClient(token=slack_token)
        self.openai_client = openai_client
        self.bot_user_id: Optional[str] = None
        self.markdown_converter = SlackMarkdownConverter()
    
    async def initialize(self):
        """Initialize bot user ID for mention detection."""
        try:
            auth_response = self.slack_client.auth_test()
            self.bot_user_id = auth_response["user_id"]
        except Exception as e:
            print(f"Failed to initialize bot: {e}")
    
    def _is_bot_mentioned(self, text: str) -> bool:
        """Check if the bot is mentioned in the message."""
        if not self.bot_user_id:
            return False
        mention_pattern = f"<@{self.bot_user_id}>"
        return mention_pattern in text
    
    def _clean_message_text(self, text: str) -> str:
        """Remove bot mentions from message text."""
        if not self.bot_user_id:
            return text
        mention_pattern = f"<@{self.bot_user_id}>"
        return text.replace(mention_pattern, "").strip()
    
    async def _get_conversation_history(self, channel: str, thread_ts: Optional[str] = None, limit: int = 15) -> List[Dict[str, str]]:
        """Get conversation history from Slack and convert to OpenAI format."""
        try:
            if thread_ts:
                # Get thread replies for channel mentions
                response = self.slack_client.conversations_replies(
                    channel=channel,
                    ts=thread_ts,
                    limit=limit
                )
                messages = response["messages"]
            else:
                # Get conversation history for DMs
                response = self.slack_client.conversations_history(
                    channel=channel,
                    limit=limit
                )
                messages = response["messages"]
            
            # Convert to OpenAI format, excluding the current message (it's the last one)
            history = []
            for msg in reversed(messages[:-1]):  # Reverse to chronological order, exclude last message
                if msg.get("bot_id") == self.bot_user_id or msg.get("user") == self.bot_user_id:
                    # Bot message
                    history.append({
                        "role": "assistant",
                        "content": msg.get("text", "")
                    })
                elif msg.get("user") and msg.get("text"):
                    # User message
                    clean_text = self._clean_message_text(msg.get("text", ""))
                    if clean_text:  # Only add non-empty messages
                        history.append({
                            "role": "user", 
                            "content": clean_text
                        })
            
            return history
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    async def handle_app_mention(self, event: Dict[str, Any]):
        """Handle when bot is mentioned in a channel."""
        channel = event["channel"]
        text = event["text"]
        # For demo purposes, don't use threads - always respond as a new message
        # thread_ts = event.get("thread_ts", event["ts"])  
        
        # Clean the message text
        clean_text = self._clean_message_text(text)
        if not clean_text:
            return
        
        # Get conversation history from channel (not thread-specific)
        history = await self._get_conversation_history(channel, None)
        
        # Get AI response
        response = await get_chat_response(self.openai_client, clean_text, history)
        
        # Convert markdown to Slack mrkdwn
        slack_response = self.markdown_converter.convert(response)
        
        # Send response as new message (not in thread)
        try:
            self.slack_client.chat_postMessage(
                channel=channel,
                text=slack_response
                # Removed thread_ts to send as new message
            )
        except Exception as e:
            print(f"Error sending message: {e}")
            # Send error response
            self.slack_client.chat_postMessage(
                channel=channel,
                text="Sorry, I encountered an error processing your request."
                # No thread_ts for demo
            )
    
    async def handle_direct_message(self, event: Dict[str, Any]):
        """Handle direct messages to the bot."""
        channel = event["channel"]  # For DMs, this is the DM channel ID
        text = event["text"]
        
        if not text.strip():
            return
        
        # Get conversation history
        history = await self._get_conversation_history(channel)
        
        # Get AI response
        response = await get_chat_response(self.openai_client, text, history)
        
        # Convert markdown to Slack mrkdwn
        slack_response = self.markdown_converter.convert(response)
        
        # Send response
        try:
            self.slack_client.chat_postMessage(
                channel=channel,
                text=slack_response
            )
        except Exception as e:
            print(f"Error sending DM: {e}")
            # Send error response
            self.slack_client.chat_postMessage(
                channel=channel,
                text="Sorry, I encountered an error processing your request."
            )
    
    async def handle_slack_event(self, event_data: Dict[str, Any]):
        """Main event handler for Slack events."""
        event = event_data.get("event", {})
        event_type = event.get("type")
        
        # Initialize bot user ID if not done yet
        if not self.bot_user_id:
            await self.initialize()
        
        # Ignore bot's own messages
        if event.get("user") == self.bot_user_id or event.get("bot_id"):
            return
        
        try:
            if event_type == "app_mention":
                await self.handle_app_mention(event)
            elif event_type == "message" and event.get("channel_type") == "im":
                await self.handle_direct_message(event)
        except Exception as e:
            print(f"Error handling Slack event: {e}")