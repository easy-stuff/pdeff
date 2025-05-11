import io
from PyPDF2 import PdfMerger


def merge_pdfs(files: list) -> io.BytesIO:
    """
    Merges a list of PDF file paths or file-like objects into a single PDF stream.

    Args:
        files (list): A list of file paths or file-like objects to PDF files.

    Returns:
        io.BytesIO: A BytesIO stream containing the merged PDF.

    Raises:
        ValueError: If the files list is empty.
        PdfReadError: If any file cannot be read as a PDF.
        Exception: For general merge or write failures.
    """
    if not files:
        raise ValueError("No PDF files provided for merging.")

    output = io.BytesIO()
    merger = PdfMerger()

    try:
        for f in files:
            try:
                merger.append(f)
            except Exception as e:
                raise Exception(f"Error appending file '{f}' to merger.") from e

        try:
            merger.write(output)
        except Exception as e:
            raise Exception("Failed to write merged PDF to output stream.") from e

        output.seek(0)
        return output

    finally:
        merger.close()
