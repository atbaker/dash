#!/usr/bin/env python3

"""
Local test script for Airtable leads function.
Tests the function with sample data before deployment.
"""

import os
import sys
from __main__ import main

def test_airtable_leads():
    """Test the Airtable leads function with sample data."""
    
    # Check environment variables
    if not os.getenv('AIRTABLE_ACCESS_TOKEN'):
        print("❌ AIRTABLE_ACCESS_TOKEN environment variable not set")
        return False
        
    if not os.getenv('AIRTABLE_BASE_ID'):
        print("❌ AIRTABLE_BASE_ID environment variable not set")
        return False
        
    if not os.getenv('AIRTABLE_TABLE_ID'):
        print("❌ AIRTABLE_TABLE_ID environment variable not set")
        return False
    
    # Test event data
    test_event = {
        'customer': 'Test Company Inc',
        'website': 'https://testcompany.example.com',
        'notes': 'This is a test lead created by the local test script. The company appears to be a software startup focused on productivity tools.'
    }
    
    print("🧪 Testing Airtable leads function...")
    print(f"Customer: {test_event['customer']}")
    print(f"Website: {test_event['website']}")
    print(f"Notes: {test_event['notes'][:50]}...")
    
    try:
        # Call the function
        result = main(test_event, {})
        
        print(f"\n📋 Function Response:")
        print(f"Status Code: {result['statusCode']}")
        print(f"Body: {result['body']}")
        
        if result['statusCode'] == 200:
            print("✅ Test passed - Lead created successfully")
            return True
        else:
            print("❌ Test failed - Function returned error")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def test_validation():
    """Test function validation with missing parameters."""
    
    print("\n🧪 Testing parameter validation...")
    
    # Test missing customer
    test_event = {
        'website': 'https://example.com',
        'notes': 'Test notes'
    }
    
    result = main(test_event, {})
    if result['statusCode'] == 400 and 'Customer parameter is required' in result['body']['error']:
        print("✅ Customer validation test passed")
    else:
        print("❌ Customer validation test failed")
        return False
    
    # Test missing website
    test_event = {
        'customer': 'Test Company',
        'notes': 'Test notes'
    }
    
    result = main(test_event, {})
    if result['statusCode'] == 400 and 'Website parameter is required' in result['body']['error']:
        print("✅ Website validation test passed")
    else:
        print("❌ Website validation test failed")
        return False
    
    # Test missing notes
    test_event = {
        'customer': 'Test Company',
        'website': 'https://example.com'
    }
    
    result = main(test_event, {})
    if result['statusCode'] == 400 and 'Notes parameter is required' in result['body']['error']:
        print("✅ Notes validation test passed")
    else:
        print("❌ Notes validation test failed")
        return False
        
    return True

if __name__ == "__main__":
    print("🚀 Running Airtable leads function tests\n")
    
    # Run validation tests first
    if not test_validation():
        print("\n❌ Validation tests failed")
        sys.exit(1)
    
    # Run main function test
    if test_airtable_leads():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)