# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API
_api_key = os.getenv("ANTHROPIC_API_KEY")
if not _api_key:
    raise ValueError("ANTHROPIC_API_KEY not found. Check your .env file.")
ANTHROPIC_API_KEY: str = _api_key

MODEL_NAME = "claude-sonnet-4-6"

# Agent behaviour
MAX_ITERATIONS = 10
TEMPERATURE = 0.3

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")