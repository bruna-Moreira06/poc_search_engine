import os

import fitz  # PyMuPDF
from elasticsearch import Elasticsearch
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialiser la connexion à ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Dossier pour stocker les fichiers uploadés
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction pour traiter un PDF


def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    doc_data = {
        "file_name": os.path.basename(pdf_path),
        "content": text,
        "is_signed": False  # Défaut à False lors de l'indexation
    }

    # Envoyer les données à ElasticSearch
    es.index(index="documents", body=doc_data)
    print(f"Document {pdf_path} traité et ajouté à ElasticSearch.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            process_pdf(filepath)
            flash('File successfully uploaded and processed')
            return redirect(url_for('index'))
    return render_template('upload.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        search_query = {
            "query": {
                "match": {
                    "content": query
                }
            }
        }
        response = es.search(index="documents", body=search_query)
        results = response['hits']['hits']
    return render_template('search.html', results=results, query=query)


@app.route('/update-signature/<doc_id>', methods=['POST'])
def update_signature(doc_id):
    # Met à jour l'attribut is_signed pour le document spécifié
    es.update(index="documents", id=doc_id, body={"doc": {"is_signed": True}})
    flash('Document signed status updated')
    return redirect(url_for('search'))


if __name__ == '__main__':
    app.run(debug=True)
