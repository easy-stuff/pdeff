import os
import typing as t
import logging
from flask import Flask, render_template, request, send_file
import utils

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    logger.debug("Rendering the home page")
    return render_template("home.html")


@app.route("/merge_pdf", methods=['GET', 'POST'])
def merge_pdf():
    if request.method == 'GET':
        logger.debug("Rendering merge PDF page")
        return render_template("merge_pdf.html")

    elif request.method == 'POST':
        logger.debug("Processing merge PDF request")
        files = request.files.getlist('files')
        filename = request.form.get('filename', 'merged')

        logger.debug(f"Received files: {len(files)}")
        logger.debug(f"Filename for the merged PDF: {filename}")

        final_name = utils.files.sanitize_filename(
            filename=filename,
            extension='.pdf'
        )
        logger.debug(f"Sanitized filename: {final_name}")

        try:
            merged_pdf = utils.pdf.merge.merge_pdfs(files=files)
            logger.debug(f"Merged {len(files)} PDF(s) successfully")
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return "Error merging PDFs", 500

        return send_file(
            merged_pdf,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/pdf'
        )


@app.route("/split_pdf", methods=['GET', 'POST'])
def split_pdf():
    if request.method == 'GET':
        logger.debug("Rendering split PDF page")
        return render_template("split_pdf.html")

    elif request.method == 'POST':
        logger.debug("Processing split PDF request")
        files = request.files.getlist('files')
        stepping = int(request.form.get('stepping', 1))

        logger.debug(f"Received files: {len(files)}")
        logger.debug(f"Stepping value: {stepping}")

        final_name = utils.files.sanitize_filename(
            filename=f"{len(files)}_pdeff_split",
            extension='.zip'
        )
        logger.debug(f"Sanitized filename: {final_name}")

        try:
            splitted_pdf = utils.pdf.split.split_pdf(
                files=files,
                stepping=stepping
            )
            logger.debug(
                f"Successfully split the PDFs into {len(splitted_pdf)} parts")
        except Exception as e:
            logger.error(f"Error splitting PDFs: {e}")
            return "Error splitting PDFs", 500

        return send_file(
            splitted_pdf,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/zip'
        )


@app.route("/compress_pdf", methods=['GET', 'POST'])
def compress_pdf():
    if request.method == 'GET':
        logger.debug("Rendering compress PDF page")
        return render_template("compress_pdf.html")

    elif request.method == 'POST':
        logger.debug("Processing compress PDF request")
        files = request.files.getlist('files')
        compression_level = request.form.get('compression_level', 'low')

        logger.debug(f"Received files: {len(files)}")
        logger.debug(f"Compression level: {compression_level}")

        final_name = utils.files.sanitize_filename(
            filename=f"{len(files)}_compressed",
            extension='.zip'
        )
        logger.debug(f"Sanitized filename: {final_name}")

        try:
            compressed_pdf = utils.pdf.compress.compress_pdf(
                files=files,
                compression_level=compression_level,
            )
            logger.debug(f"Successfully compressed {len(files)} PDF(s)")
        except Exception as e:
            logger.error(f"Error compressing PDFs: {e}")
            return "Error compressing PDFs", 500

        return send_file(
            compressed_pdf,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/zip'
        )


@app.route("/to_docx", methods=['GET', 'POST'])
def to_docx():
    if request.method == 'GET':
        logger.debug("Rendering to DOCX page")
        return render_template("to_docx.html")

    elif request.method == 'POST':
        logger.debug("Processing to DOCX request")
        files = request.files.getlist('files')
        use_ocr = request.form.get('use_ocr', 'no')

        logger.debug(f"Received files: {len(files)}")
        logger.debug(f"OCR Use: {use_ocr}")

        final_name = utils.files.sanitize_filename(
            filename=f"{len(files)}_to_docx",
            extension='.zip'
        )
        logger.debug(f"Sanitized filename: {final_name}")

        try:
            if use_ocr == 'no':
                converted_docx = utils.pdf.docx.to_docx_no_ocr(
                    files=files,
                )
            else:
                converted_docx = utils.pdf.docx.to_docx_ocr(
                    files=files,
                )
            logger.debug(f"Successfully converted {len(files)} PDF(s)")
        except Exception as e:
            logger.error(f"Error converting PDFs: {e}")
            return "Error converting PDFs", 500

        return send_file(
            converted_docx,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/zip'
        )

@app.route("/from_docx", methods=['GET', 'POST'])
def from_docx():
    if request.method == 'GET':
        logger.debug("Rendering compress PDF page")
        return render_template("from_docx.html")

    elif request.method == 'POST':
        logger.debug("Processing compress PDF request")
        files = request.files.getlist('files')

        logger.debug(f"Received files: {len(files)}")

        final_name = utils.files.sanitize_filename(
            filename=f"{len(files)}_from_docx_to_pdf",
            extension='.zip'
        )
        logger.debug(f"Sanitized filename: {final_name}")

        try:
            compressed_pdf = utils.pdf.docx.to_pdf(
                files=files,
            )
            logger.debug(f"Successfully compressed {len(files)} PDF(s)")
        except Exception as e:
            logger.error(f"Error compressing PDFs: {e}")
            return "Error compressing PDFs", 500

        return send_file(
            compressed_pdf,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/zip'
        )

if __name__ == "__main__":
    logger.info("Starting the Flask app in debug mode")
    app.run("0.0.0.0", port=8080, debug=True)
