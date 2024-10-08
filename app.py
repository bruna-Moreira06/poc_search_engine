import os
import fitz  # PyMuPDF pour manipuler les fichiers PDF
from elasticsearch import Elasticsearch
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
import sqlite3
from flask import g
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

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
    doc = fitz.open(pdf_path) 
    text = "" 
    for page in doc:
        text += page.get_text()
    doc_data = {
        "file_name": os.path.basename(pdf_path),
        "content": text,
        "is_signed": False
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

        # Hacher le mot de passe avant de l'enregistrer dans la base de données
        hashed_password = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user (username, email, password, role_id) VALUES (?, ?, ?, ?)",
                    (username, email, hashed_password, role_id))
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
        file = request.files['file']

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO documents (name_doc, uploaded_by, is_signed)
                VALUES (?, ?, ?)
            """, (filename, uploaded_by, is_signed))
            db.commit()

            flash('Document uploaded successfully')
            return redirect(url_for('index'))
        flash('No file selected or invalid file name')
    
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
        cursor.execute("SELECT * FROM documents WHERE name_doc LIKE ?", ('%' + query + '%',))
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
        cursor.execute("INSERT INTO roles (id, name_roles, description) VALUES (?, ?, ?)",
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
        cursor.execute("INSERT INTO permissions (id, name_permissions) VALUES (?, ?)",
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
        cursor.execute("INSERT INTO labels (name_labels) VALUES (?)", (name,))
        db.commit()

        flash('Tag added successfully')
        return redirect(url_for('index'))
    return render_template('add_etiquettes.html')

def delete_document(document_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    db.commit()

    es.delete(index="documents", id=document_id)

    print(f"Document {document_id} supprimé de SQLite et Elasticsearch.")


# Lancer l'application Flask en mode debug
if __name__ == '__main__':
    app.run(debug=True)
