from datetime import datetime, timezone
import re

RANGE_PATTERN = r"^\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}$"
DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

# Detect the type of query (student_id, staff_id, date_range, date, or service).
# Args: query: The query string to analyze
# Returns: str: The detected query type
def detect_query_type(query):
    # Student ID
    if query.isdigit() and query.startswith("8160") and len(query) == 9:
        return "student"

    # Staff ID
    if query.isdigit() and query.startswith("3") and len(query) == 9:
        return "staff"

    # Date range
    if re.match(RANGE_PATTERN, query):
        try:
            start_str, end_str = query.split(":")
            datetime.strptime(start_str, "%Y-%m-%d")
            datetime.strptime(end_str, "%Y-%m-%d")
            return "date_range"
        except ValueError:
            pass

    # Single date
    if re.match(DATE_PATTERN, query):
        try:
            datetime.strptime(query, "%Y-%m-%d")
            return "date"
        except ValueError:
            pass

    # Fallback: treat as service string
    return "service"
