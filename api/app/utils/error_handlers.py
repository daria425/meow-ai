def categorize_error(error: str) -> str:
    """Categorize error message for better handling.
    Args:
        error: Error message string
    Returns:
        Error category identifier
    Examples:
        >>> categorize_error("Connection timeout after 30s")
        'TIMEOUT'
        >>> categorize_error("API rate limit exceeded")
        'RATE_LIMIT'
    """
    if "timeout" in error.lower():
        return "TIMEOUT"
    elif "rate limit" in error.lower():
        return "RATE_LIMIT"
    elif "permission" in error.lower():
        return "PERMISSION"
    elif "parsing" in error.lower():
        return "PARSE_ERROR"
    return "UNKNOWN"