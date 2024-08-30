import os
import fitz  # PyMuPDF pour manipuler les fichiers PDF
from elasticsearch import Elasticsearch
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
import sqlite3
from flask import g
from werkzeug.utils import secure_filename

# Initialiser l'application Flask
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Clé secrète pour les sessions Flask

# Initialiser la connexion à Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

DATABASE = 'poc_search_engine.db'

def get_db():
    conn = sqlite3.connect('poc_search_engine.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user (username, email, password, role_id) VALUES (?, ?, ?, ?)",
                    (username, email, password, role_id))
        db.commit()
        flash('User added successfully')
        return redirect(url_for('index'))
    return render_template('add_user.html')

# Route pour uploader un fichier PDF
@app.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if request.method == 'POST':
        uploaded_by = 1
        is_signed = 0

        # Récupérer le fichier uploadé
        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Connexion à la base de données
            db = get_db()
            cursor = db.cursor()

            # Insertion des informations dans la base de données
            cursor.execute("""
                INSERT INTO documents (name, uploaded_by, is_signed)
                VALUES (?, ?, ?)
            """, (filename, uploaded_by, is_signed))
            db.commit()

            # Message de confirmation
            flash('Document uploaded successfully')

            # Redirection vers une page (ex: liste des documents)
            return redirect(url_for('list_documents'))

        flash('No file selected or invalid file name')
    
    # Affichage du formulaire d'upload
    return render_template('upload.html')

# Route pour rechercher des documents dans Elasticsearch
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = ""
    results = []
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        query = request.form['query']
        cursor.execute("SELECT * FROM documents WHERE document_name LIKE ?", ('%' + query + '%',))
    else:
        cursor.execute("SELECT * FROM documents")

    results = cursor.fetchall()

    return render_template('search.html', query=query, results=[dict(row) for row in results])



# Route pour mettre à jour le statut "signé" d'un document
@app.route('/update_signature/<doc_id>', methods=['POST'])
def update_signature(doc_id):
    # Met à jour l'attribut is_signed pour le document spécifié
    es.update(index="documents", id=doc_id, body={"doc": {"is_signed": True}})
    flash('Document signed status updated')
    return redirect(url_for('search'))  # Redirige vers la page de recherche


# Route pour ajouter un rôle
@app.route('/add_role', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        description = request.form['description']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO roles (id, name, description) VALUES (?, ?, ?)",
                    (id, name, description))
        db.commit()
        flash('User added successfully')
        return redirect(url_for('index'))
    return render_template('add_role.html')

@app.route('/add_permissions', methods=['GET', 'POST'])
def add_permissions():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO permissions (id, name) VALUES (?, ?)",
                    (id, name))
        db.commit()
        flash('User added successfully')
        return redirect(url_for('index'))
    return render_template('add_permissions.html')

@app.route('/assign_permission', methods=['GET', 'POST'])
def assign_permission():
    if request.method == 'POST':
        role_id = request.form['role_id']
        permission_id = request.form['permission_id']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)",
                       (role_id, permission_id))
        db.commit()

        flash('Permission assigned to role successfully')
        return redirect(url_for('index'))
    return render_template('add_permissions_roles.html')

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        name = request.form['name']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO labels (name) VALUES (?)", (name))
        db.commit()

        flash('Tag added successfully')
        return redirect(url_for('index'))
    return render_template('add_etiquettes.html')


# Lancer l'application Flask en mode debug
if __name__ == '__main__':
    app.run(debug=True)
