import re
import os


def sanitize_filename(filename: str, extension: str, max_length: int = 255) -> str:
    """
    Sanitize a filename to be safe for both Windows and Linux filesystems,
    and ensure it ends with the given extension.

    Args:
        filename (str): Original filename (can include extension or not).
        extension (str): Desired extension (with or without leading dot).
        max_length (int): Optional maximum length for the filename. Default is 255.

    Returns:
        str: A sanitized and safe filename ending with the given extension.
    """
    # Normalize extension
    if not extension.startswith('.'):
        extension = '.' + extension

    # Remove path parts (security and cleanliness)
    filename = os.path.basename(filename)

    # Remove illegal characters for Windows and Linux
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

    # Remove control characters and strip trailing spaces/dots
    filename = filename.strip().strip('.').strip()

    # Remove existing extension if it doesn't match the desired one
    if filename.lower().endswith(extension.lower()):
        filename = filename[:-len(extension)]

    # Collapse repeated underscores
    filename = re.sub(r'_+', '_', filename)

    # Truncate if too long
    base_max = max_length - len(extension)
    filename = filename[:base_max]

    # Ensure not empty
    if not filename:
        filename = "file"

    # Add desired extension
    return filename + extension
