import os
import re
from datetime import datetime

def validate_date(date_str):
    """
    Validate that a string is in the correct date format (YYYY-MM-DD).
    
    Args:
        date_str: String to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic format validation using regex
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return False
    
    # Validate it can be parsed as a date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def clear_screen():
    """Clear the terminal screen."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux
    else:
        os.system('clear')

def format_date_for_display(date_str):
    """
    Format a date string for display.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        str: Formatted date string (e.g., "January 1, 2023")
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except (ValueError, TypeError):
        return date_str  # Return original if formatting fails
