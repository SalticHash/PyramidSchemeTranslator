from translate import translate
import vercel_blob
from uuid import uuid4
from dotenv import load_dotenv
from random import choices
from string import ascii_letters, digits
load_dotenv()

# builtins
from io import BytesIO
# Flask Imports
from werkzeug.datastructures import FileStorage
from flask import Flask, render_template, request, send_file, redirect, Response

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

    name = generated_posters.filename.rstrip(".pdf")
    suffix = "".join(choices(ascii_letters + digits, k = 8))
    filename = name + "." + suffix + ".pdf"
    resp = vercel_blob.put(filename, pdf_bytes)
    
    return redirect(resp['url'])
    
@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5454)