import io
import zipfile
import logging
from PyPDF2 import PdfReader, PdfWriter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def split_pdf(files: list, stepping: int) -> io.BytesIO:
    """
    Splits a list of PDF files into smaller PDFs, each containing a specified number of pages.

    Args:
        files (list): A list of file-like objects to PDF files.
        stepping (int): The number of pages per split PDF.

    Returns:
        io.BytesIO: A BytesIO stream containing the split PDFs in a ZIP archive.

    Raises:
        Exception: For general split or zip failures.
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for index, file in enumerate(files):
            # Important: reset file pointer
            file.seek(0)

            try:
                reader = PdfReader(file)
                logger.debug(f"Successfully read PDF {file.filename}.")
            except Exception as e:
                logger.error(f"Error reading PDF {file.filename}: {e}")
                continue  # Skip unreadable files

            total_pages = len(reader.pages)
            if total_pages == 0:
                logger.warning(f"Skipping empty PDF: {file.filename}")
                continue

            base_name = getattr(
                file, 'filename', f'file_{index}').rsplit('.', 1)[0]

            for i in range(0, total_pages, stepping):
                writer = PdfWriter()

                for j in range(i, min(i + stepping, total_pages)):
                    writer.add_page(reader.pages[j])

                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)

                part_name = f"{base_name}_p{i+1}_to_p{min(i+stepping, total_pages)}.pdf"

                # Add to zip
                try:
                    zip_file.writestr(part_name, output_pdf.read())
                    logger.debug(f"Added part {part_name} to ZIP.")
                except Exception as e:
                    logger.error(f"Failed to add {part_name} to ZIP: {e}")
                    continue

    zip_buffer.seek(0)
    logger.debug("PDF split complete, returning ZIP buffer.")
    return zip_buffer
