from flask import Flask, request, jsonify
import PyPDF2
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

DOCUMENT_TEXT = ""

# ---------- PDF READER ----------
@app.route("/upload/pdf", methods=["POST"])
def upload_pdf():
    global DOCUMENT_TEXT
    file = request.files["file"]

    reader = PyPDF2.PdfReader(file)
    DOCUMENT_TEXT = ""

    for page in reader.pages:
        DOCUMENT_TEXT += page.extract_text()

    return jsonify({"message": "PDF processed successfully"})

# ---------- IMAGE OCR ----------
@app.route("/upload/image", methods=["POST"])
def upload_image():
    global DOCUMENT_TEXT
    image = Image.open(request.files["file"])
    DOCUMENT_TEXT = pytesseract.image_to_string(image)

    return jsonify({"message": "Image processed successfully"})

# ---------- SUMMARY ----------
@app.route("/summary", methods=["GET"])
def summary():
    level = request.args.get("level", "short")
    sentences = DOCUMENT_TEXT.split(".")

    if level == "short":
        data = sentences[:3]
    elif level == "medium":
        data = sentences[:8]
    else:
        data = sentences[:15]

    return jsonify({"summary": data})

# ---------- QUESTION ANSWER ----------
@app.route("/ask", methods=["POST"])
def ask():
    question = request.json["question"].lower()
    keywords = question.split()

    for sentence in DOCUMENT_TEXT.split("."):
        for word in keywords:
            if word in sentence.lower():
                return jsonify({"answer": sentence})

    return jsonify({"answer": "Answer not found"})

# ---------- WORD FREQUENCY CHART ----------
@app.route("/chart", methods=["GET"])
def chart():
    words = DOCUMENT_TEXT.lower().split()
    freq = {}

    for w in words:
        if w.isalpha():
            freq[w] = freq.get(w, 0) + 1

    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:7]
    labels = [i[0] for i in top]
    values = [i[1] for i in top]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Word Frequency")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    encoded = base64.b64encode(img.read()).decode()
    plt.close()

    return jsonify({"image": encoded})

if __name__ == "__main__":
    app.run(debug=True)
