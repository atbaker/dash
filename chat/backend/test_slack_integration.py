#!/usr/bin/env python3
"""
Basic test script for Slack bot integration.
Run this to verify imports and basic initialization work correctly.
"""
import sys
import os
from unittest.mock import Mock

def test_imports():
    """Test that all modules can be imported."""
    try:
        from chat_service import get_chat_response, stream_chat_response
        from slack_bot import SlackBot
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_slack_bot_init():
    """Test Slack bot initialization."""
    try:
        from slack_bot import SlackBot
        
        # Mock OpenAI client
        mock_client = Mock()
        
        # Test initialization
        bot = SlackBot("test-token", mock_client)
        print("✓ SlackBot initialized successfully")
        
        # Test message cleaning
        clean_msg = bot._clean_message_text("<@U123456> Hello there!")
        print(f"✓ Message cleaning works: '{clean_msg}'")
        
        return True
    except Exception as e:
        print(f"✗ SlackBot initialization error: {e}")
        return False

def test_chat_service():
    """Test chat service functions exist."""
    try:
        from chat_service import get_chat_response, stream_chat_response
        print("✓ Chat service functions available")
        return True
    except Exception as e:
        print(f"✗ Chat service error: {e}")
        return False

def test_main_app():
    """Test main app can be imported."""
    try:
        # Temporarily set required env vars
        os.environ['DO_AGENT_ENDPOINT'] = 'test'
        os.environ['DO_AGENT_ACCESS_KEY'] = 'test'
        
        import main
        print("✓ Main FastAPI app imported successfully")
        print(f"✓ Slack enabled: {main.slack_bot is not None}")
        return True
    except Exception as e:
        print(f"✗ Main app error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Slack bot integration...")
    print("-" * 40)
    
    tests = [
        test_imports,
        test_slack_bot_init, 
        test_chat_service,
        test_main_app
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    if all(results):
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)