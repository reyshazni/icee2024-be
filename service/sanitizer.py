import re

def filename_url_sanitizer(filename):
    # Replace characters that could conflict with URLs with "_"
    sanitized_filename = re.sub(r'[^\w.-]', '_', filename)
    return sanitized_filename.lower()