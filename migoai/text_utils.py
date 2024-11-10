import textwrap
from .config import MAX_WIDTH

def wrap_text(text, width=MAX_WIDTH):
    """Wrap text to specified width."""
    return '\n'.join(textwrap.wrap(text, width=width, replace_whitespace=False))

def clean_text(text):
    """Clean and normalize text to handle special characters.""" 
    return text.encode('utf-8').decode('utf-8', 'replace')