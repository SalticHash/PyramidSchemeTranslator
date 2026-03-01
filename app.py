from translate import translate
from uuid import uuid4
from dotenv import load_dotenv
from os import getenv
from requests import post
from vercel.blob import ?!?!?!
from requests import get as get_blob
load_dotenv()
BLOB_TOKEN = getenv("PS_TRANSLATOR_READ_WRITE_TOKEN")

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
    body = request.get_json()
    generated_posters: BytesIO = get_blob(body["generated_posters_url"]).content
    translated_poster: BytesIO = get_blob(body["translated_poster_url"]).content
    
    pdf_bytes = translate(generated_posters, translated_poster)
    if type(pdf_bytes) == str:
        return error(pdf_bytes, 400)

    filename = "output/" + str(uuid4()) + ".pdf"
    response = put_blob(filename, pdf_bytes)
    
    return response.get("url")
    
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


@app.route("/api/blob_upload_url")
def blob_upload_url():

    res = post(
        "https://blob.vercel-storage.com/upload",
        headers={
            "Authorization": f"Bearer {BLOB_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "pathname": "uploads/input.pdf",
            "access": "public"
        }
    )

    return jsonify(res.json())

if __name__ == "__main__":
    app.run(port=5454, debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5454)