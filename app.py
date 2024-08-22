import os
import fitz  # PyMuPDF pour manipuler les fichiers PDF
from elasticsearch import Elasticsearch
from flask import Flask, flash, redirect, render_template, request, url_for

# Initialiser l'application Flask
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Clé secrète pour les sessions Flask

# Initialiser la connexion à Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Dossier pour stocker les fichiers uploadés
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crée le dossier s'il n'existe pas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction pour traiter un PDF et l'indexer dans Elasticsearch
def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Ouvre le fichier PDF
    text = ""  # Variable pour stocker le texte extrait du PDF

    # Parcourt chaque page du PDF et extrait le texte
    for page in doc:
        text += page.get_text()

    # Crée un dictionnaire avec les données du document
    doc_data = {
        "file_name": os.path.basename(pdf_path),  # Nom du fichier PDF
        "content": text,  # Contenu textuel du PDF
        "is_signed": False  # Statut par défaut du document (non signé)
    }

    # Indexe le document dans Elasticsearch
    es.index(index="documents", body=doc_data)
    print(f"Document {pdf_path} traité et ajouté à Elasticsearch.")

# Route principale pour afficher la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour uploader un fichier PDF
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':  # Si la méthode est POST (formulaire soumis)
        if 'file' not in request.files:
            flash('No file part')  # Alerte si aucun fichier n'est sélectionné
            return redirect(request.url)
        file = request.files['file']  # Récupère le fichier uploadé
        if file.filename == '':
            flash('No selected file')  # Alerte si aucun fichier n'est choisi
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            # Si le fichier est un PDF valide
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)  # Sauvegarde le fichier sur le serveur
            process_pdf(filepath)  # Traite et indexe le PDF
            flash('File successfully uploaded and processed')
            return redirect(url_for('index'))  # Redirige vers l'accueil
    return render_template('upload.html')  # Affiche la page d'upload

# Route pour rechercher des documents dans Elasticsearch
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
    else:
        # Récupère tous les documents si la méthode n'est pas POST
        response = es.search(index="documents", body={"query": {"match_all": {}}})
        results = response['hits']['hits']

    return render_template('search.html', results=results, query=query)


# Route pour mettre à jour le statut "signé" d'un document
@app.route('/update-signature/<doc_id>', methods=['POST'])
def update_signature(doc_id):
    # Met à jour l'attribut is_signed pour le document spécifié
    es.update(index="documents", id=doc_id, body={"doc": {"is_signed": True}})
    flash('Document signed status updated')  # Alerte de succès
    return redirect(url_for('search'))  # Redirige vers la page de recherche

@app.route('/documents')
def show_documents():
    # Requête pour récupérer tous les documents indexés dans Elasticsearch
    response = es.search(index="documents", body={"query": {"match_all": {}}})
    all_documents = response['hits']['hits']  # Récupère tous les documents
    return render_template('documents.html', documents=all_documents)

# Lancer l'application Flask en mode debug
if __name__ == '__main__':
    app.run(debug=True)
