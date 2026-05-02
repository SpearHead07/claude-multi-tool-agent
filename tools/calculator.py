# tools/calculator.py
from src.logger import get_logger

log = get_logger(__name__)


def calculator(expression: str) -> str:
    """Safely evaluate a math expression. Returns result as string."""
    log.info(f"calculator called with: {expression}")

    allowed = set("0123456789+-*/()., ")
    if not all(c in allowed for c in expression):
        log.warning(f"calculator rejected invalid expression: {expression}")
        return "Error: invalid characters in expression"

    try:
        result = eval(expression)
        log.info(f"calculator result: {result}")
        return f"{expression} = {result}"
    except Exception as e:
        log.error(f"calculator failed: {e}")
        return f"Error: {str(e)}"


SCHEMA = {
    "name": "calculator",
    "description": (
        "Performs mathematical calculations. Use this when the user asks to compute, "
        "add, subtract, multiply, divide, or evaluate any math expression. "
        "Do NOT use for date or text questions."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A math expression e.g. '4*7' or '(100/5)+3'",
            }
        },
        "required": ["expression"],
    },
}