from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/merge_pdf", methods=['GET', 'POST'])
def merge_pdf():
    if request.method == 'GET':
        return render_template("merge_pdf.html")

    elif request.method == 'POST':
        # get the files
        # store all the files in the order which im supposed to merge in a variable
        # and also get the filename
        ...


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
