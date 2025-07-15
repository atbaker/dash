"""
SQL utility functions for query validation and data serialization.
"""
import re
from datetime import datetime, date
from decimal import Decimal


def convert_to_json_serializable(obj):
    """
    Convert PostgreSQL types to JSON-serializable Python types.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, memoryview):
        return obj.tobytes().hex()
    elif isinstance(obj, bytes):
        return obj.hex()
    elif obj is None:
        return None
    else:
        # For any other type, try converting to string
        return str(obj)


def serialize_row(row):
    """
    Convert all values in a row to JSON-serializable types.
    """
    return {key: convert_to_json_serializable(value) if not isinstance(value, (str, int, float, bool, type(None))) else value
            for key, value in row.items()}


def is_read_only_query(query):
    """
    Check if a SQL query is read-only (SELECT only).
    """
    # Remove comments and normalize whitespace
    cleaned = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip().upper()
    
    # Check if query starts with SELECT or WITH (for CTEs)
    if not (cleaned.startswith('SELECT') or cleaned.startswith('WITH')):
        return False
    
    # List of forbidden keywords that indicate write operations
    forbidden_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
    
    # Check for forbidden keywords as whole words to avoid false positives
    for keyword in forbidden_keywords:
        if re.search(r'\b' + keyword + r'\b', cleaned):
            return False
    
    return True