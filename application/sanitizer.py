

def sanitize(input: str):
    """
    Sanitizer for input into mongo queries
    removes mongo key characters ("$", ";")

    Returns:
        sanitized string
    """
    forbiddenChars = ["$", ";"]
    for c in forbiddenChars:
        input = input.replace(c, "")
    return input