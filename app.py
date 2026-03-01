from translate import translate
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

# builtins
from io import BytesIO
# Flask Imports
from werkzeug.datastructures import FileStorage
from flask import Flask, render_template, request, send_file, Response

# Configure application
app = Flask(__name__)

def is_pdf(filename: str):
    return filename.endswith(".pdf")
           
# Routes
@app.route("/translate", methods=["POST"])
def tranlate_poster() -> Response:
    generated_posters: FileStorage = request.files["generated_posters"]
    translated_poster: FileStorage = request.files["translated_poster"]
    
    pdf_bytes = translate(generated_posters.stream.read(), translated_poster.stream.read())
    if type(pdf_bytes) == str:
        return error(pdf_bytes, 400)
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=False,
        download_name="result.pdf"
    )
    
@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(_ev):
    return error("Page not found, It's nowhere to be seen", 404)

@app.errorhandler(405)
def method_not_allowed(_ev):
    return error("The method is not allowed for the requested URL.", 405)

def error(text, statuscode = 400):
    req = {"text": text, "statuscode": statuscode}
    return render_template("error.html", req=req)

if __name__ == "__main__":
    app.run(port=5454, debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5454)