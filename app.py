from translate import translate
from uuid import uuid4
from dotenv import load_dotenv
from os import getenv
from tempfile_wrapper import put_blob, get_blob, get_bytes
load_dotenv()

# builtins
from io import BytesIO
# Flask Imports
from werkzeug.datastructures import FileStorage
from flask import Flask, render_template, request, redirect, Response, jsonify

# Configure application
app = Flask(__name__)

def is_pdf(filename: str):
    return filename.endswith(".pdf")
           
# Routes
@app.route("/api/translate", methods=["POST"])
def tranlate_poster() -> Response:
    body = request.form
    generated_posters: dict = get_blob(body["generated_posters_url"])
    translated_poster: dict = get_blob(body["translated_poster_url"])
    if not generated_posters.get("success", False) or not translated_poster.get("success", False):
        return error("There was an error during the retrieving of hosted files!", 400)
    
    
    
    pdf_bytes = translate(get_bytes(generated_posters), get_bytes(translated_poster))
    if type(pdf_bytes) == str:
        return error(pdf_bytes, 400)

    filename = str(uuid4()) + ".pdf"
    response = put_blob(filename, pdf_bytes)
    
    return response["files"][0]["url"]
    
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
    # app.run(port=5454, debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5454)