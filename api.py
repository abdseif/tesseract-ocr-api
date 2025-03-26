from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    pdf_bytes = file.read()

    try:
        images = convert_from_bytes(pdf_bytes)
    except Exception as e:
        return jsonify({"error": f"PDF conversion failed: {str(e)}"}), 500

    extracted_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        extracted_text += text + "\n---PAGE BREAK---\n"

    return jsonify({"text": extracted_text})
