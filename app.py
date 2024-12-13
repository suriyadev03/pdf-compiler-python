from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (React frontend can access Flask)

@app.route('/')
def home():
    return "Flask server is working!"
    
@app.route('/upload', methods=['POST'])
def upload_files():
    # Check if the request contains both pdf1 and pdf2
    if 'pdf1' not in request.files or 'pdf2' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # Get the PDF files
    file1 = request.files['pdf1']
    file2 = request.files['pdf2']

    # Extract text from both PDFs
    text1 = extract_text_from_pdf(file1)
    text2 = extract_text_from_pdf(file2)

    # Return the extracted text as JSON response
    return jsonify({'text1': text1, 'text2': text2})

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(stream=pdf_path.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
