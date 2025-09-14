from pathlib import Path

def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"
