from flask import Flask
from flask import render_template, request, send_file
import utils

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/merge_pdf", methods=['GET', 'POST'])
def merge_pdf():
    if request.method == 'GET':
        return render_template("merge_pdf.html")

    elif request.method == 'POST':
        files = request.files.getlist('files')
        filename = request.form.get('filename', 'merged')

        final_name = utils.files.sanitize_filename(
            filename=filename,
            extension='.pdf'
        )

        merged_pdf = utils.pdf.merge.merge_pdfs(files=files)

        return send_file(
            merged_pdf,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/pdf'
        )


@app.route("/split_pdf", methods=['GET', 'POST'])
def split_pdf():
    if request.method == 'GET':
        return render_template("split_pdf.html")

    elif request.method == 'POST':
        files = request.files.getlist('files')
        stepping = int(request.form.get('stepping', 1))

        final_name = utils.files.sanitize_filename(
            filename=f"{len(files)}_pdeff_split",
            extension='.zip'
        )

        splitted_pdf = utils.pdf.split.split_pdf(
            files=files,
            stepping=stepping
        )

        return send_file(
            splitted_pdf,
            as_attachment=True,
            download_name=final_name,
            mimetype='application/zip'
        )


@app.route("/compress_pdf", methods=['GET', 'POST'])
def compress_pdf():
    if request.method == 'GET':
        return render_template("compress_pdf.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
