import typing as t
import io
import os
import zipfile
import tempfile
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def compress_pdf(files: list, compression_level: t.Literal['low', 'medium', 'high']) -> io.BytesIO:
    """
    Compresses a list of PDF files using Ghostscript and returns a zip archive
    of the compressed PDFs.

    Args:
        files (list): A list of file-like objects representing the PDF files to be compressed.
        compression_level (Literal['low', 'medium', 'high']): The level of compression to apply,
            where 'low' provides the highest quality and 'high' provides the smallest file size.

    Returns:
        io.BytesIO: A BytesIO stream containing a zip archive of the compressed PDF files.

    Raises:
        Exception: If there is an error during file processing, compression, or zipping.
    """

    logger.debug(f"Starting PDF compression with level: {compression_level}")

    zip_buffer = io.BytesIO()

    level_to_gs = {
        'low': '/screen',
        'medium': '/ebook',
        'high': '/prepress'
    }

    gs_quality = level_to_gs.get(compression_level, '/ebook')
    logger.debug(f"Ghostscript quality set to: {gs_quality}")

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file, tempfile.TemporaryDirectory() as tmpdir:
        for index, file in enumerate(files):
            logger.debug(
                f"Processing file {index + 1}/{len(files)}: {file.filename}")

            file.seek(0)
            original_path = os.path.join(tmpdir, f"original_{index}.pdf")
            compressed_path = os.path.join(tmpdir, f"compressed_{index}.pdf")

            # Write the original file to disk
            try:
                with open(original_path, 'wb') as f:
                    f.write(file.read())
                logger.debug(
                    f"Saved original file {file.filename} to {original_path}")
            except Exception as e:
                logger.error(
                    f"Error writing file {file.filename} to disk: {e}")
                continue

            # Ghostscript command with better compression control
            cmd = [
                'gswin64',  # Or 'gs' on Linux/macOS
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={gs_quality}',
                '-dDownsampleColorImages=true',
                '-dColorImageResolution=100' if compression_level == 'medium' else '-dColorImageResolution=72',
                '-dGrayImageResolution=100' if compression_level == 'medium' else '-dGrayImageResolution=72',
                '-dMonoImageResolution=150',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-sOutputFile={compressed_path}',
                original_path
            ]

            try:
                logger.debug(
                    f"Running Ghostscript command for {file.filename}")
                subprocess.run(cmd, check=True)
                logger.debug(
                    f"Compression of {file.filename} completed successfully.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Ghostscript failed on {file.filename}: {e}")
                continue

            # Read the compressed file content
            try:
                with open(compressed_path, 'rb') as f:
                    content = f.read()
                logger.debug(
                    f"Compressed file {file.filename} and added to zip.")
            except Exception as e:
                logger.error(
                    f"Error reading compressed file {file.filename}: {e}")
                continue

            base_name = getattr(
                file, 'filename', f'file_{index}').rsplit('.', 1)[0]
            zip_name = f"{base_name}_{compression_level}_compressed.pdf"
            try:
                zip_file.writestr(zip_name, content)
                logger.debug(
                    f"File {file.filename} added to zip as {zip_name}")
            except Exception as e:
                logger.error(f"Error adding file {file.filename} to zip: {e}")

            # Optional explicit cleanup
            try:
                os.remove(original_path)
                os.remove(compressed_path)
                logger.debug(f"Cleaned up temporary files for {file.filename}")
            except Exception as e:
                logger.error(f"Cleanup failed for {file.filename}: {e}")

    zip_buffer.seek(0)
    logger.debug("Compression process completed, returning the zip buffer.")
    return zip_buffer
