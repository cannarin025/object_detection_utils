
def get_substring(text, start, end):
    """
    Function to get all text between 1st occurence of start and end strings
    """
    start_marker = text.find(start)
    end_marker = text.find(end)
    return text[start_marker + len(start) : end_marker]