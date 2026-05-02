# tools/date_tool.py
from datetime import datetime
from src.logger import get_logger

log = get_logger(__name__)


def get_current_date() -> str:
    """Returns today's date and day of week."""
    log.info("get_current_date called")
    now = datetime.now()
    result = now.strftime("Today is %A, %d %B %Y")
    log.info(f"get_current_date returned: {result}")
    return result


SCHEMA = {
    "name": "get_current_date",
    "description": (
        "Returns the current date and day of the week. "
        "Use this when the user asks about today's date, the current day, "
        "or anything time-related. Takes no arguments."
    ),
    "input_schema": {
        "type": "object",
        "properties": {},
    },
}