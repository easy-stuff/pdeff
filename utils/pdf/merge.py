import io
import logging
from PyPDF2 import PdfMerger

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
        logger.error("No PDF files provided for merging.")
        raise ValueError("No PDF files provided for merging.")

    logger.debug(f"Starting to merge {len(files)} PDF files.")

    output = io.BytesIO()
    merger = PdfMerger()

    try:
        for index, f in enumerate(files):
            logger.debug(f"Appending file {index + 1}/{len(files)}: {f}")
            try:
                merger.append(f)
                logger.debug(f"Successfully appended file {f}")
            except Exception as e:
                logger.error(f"Error appending file '{f}' to merger: {e}")
                raise Exception(
                    f"Error appending file '{f}' to merger.") from e

        try:
            logger.debug("Writing merged PDF to output stream.")
            merger.write(output)
            logger.debug("Merged PDF written successfully.")
        except Exception as e:
            logger.error(f"Failed to write merged PDF to output stream: {e}")
            raise Exception(
                "Failed to write merged PDF to output stream.") from e

        output.seek(0)
        logger.debug("PDF merge complete, returning merged PDF stream.")
        return output

    finally:
        merger.close()
        logger.debug("PdfMerger closed.")
