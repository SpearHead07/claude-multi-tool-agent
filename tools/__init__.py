# tools/__init__.py
from tools.calculator import calculator, SCHEMA as CALC_SCHEMA
from tools.date_tool import get_current_date, SCHEMA as DATE_SCHEMA

ALL_SCHEMAS = [CALC_SCHEMA, DATE_SCHEMA]

REGISTRY = {
    "calculator": calculator,
    "get_current_date": get_current_date,
}