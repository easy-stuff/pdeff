import io
import os
import zipfile
import tempfile
import typing as t
import logging

import fitz  # PyMuPDF
from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def pdf_to_jpeg(files: list) -> io.BytesIO:
    logger.debug("Starting PDF to JPEG conversion")

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        with tempfile.TemporaryDirectory() as tmpdir:
            for index, file in enumerate(files):
                try:
                    filename = getattr(file, 'filename', f'file_{index}.pdf')
                    base_name = os.path.splitext(filename)[0]
                    logger.debug(f"Processing file: {filename}")

                    # Save uploaded PDF to temp
                    file_path = os.path.join(tmpdir, filename)
                    file.seek(0)
                    with open(file_path, 'wb') as f:
                        f.write(file.read())
                    logger.debug(f"Saved PDF to: {file_path}")

                    # Open PDF and convert each page
                    doc = fitz.open(file_path)
                    for i, page in enumerate(doc):
                        pix = page.get_pixmap(dpi=200, alpha=False)
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        
                        img_io = io.BytesIO()
                        img.save(img_io, format='JPEG', quality=90)
                        img_io.seek(0)

                        img_name = f"{base_name}_page_{i + 1}.jpg"
                        zip_file.writestr(img_name, img_io.read())
                        logger.debug(f"Added image to ZIP: {img_name}")

                    doc.close()

                except Exception as e:
                    logger.exception(f"Error processing {filename}: {e}")

    zip_buffer.seek(0)
    logger.debug("Returning zipped JPEG images as BytesIO")
    return zip_buffer
