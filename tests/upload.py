import os
import tempfile
import unittest
from flask import Flask
from werkzeug.datastructures import FileStorage
from myapp import app, get_db 

class UploadDocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db = get_db()
            db.executescript('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_doc TEXT NOT NULL,
                    uploaded_by INTEGER NOT NULL,
                    is_signed INTEGER NOT NULL
                );
            ''')

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        os.rmdir(app.config['UPLOAD_FOLDER'])

    def test_upload_document_success(self):
        data = {
            'file': (FileStorage(
                stream=open(__file__, 'rb'),
                filename='test.pdf',
                content_type='application/pdf'
            ), 'test.pdf')
        }

        response = self.app.post('/upload_document', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 302)

        saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test.pdf')
        self.assertTrue(os.path.exists(saved_file_path))

        with app.app_context():
            db = get_db()
            cursor = db.execute("SELECT * FROM documents WHERE name_doc = 'test.pdf'")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result['uploaded_by'], 1)
            self.assertEqual(result['is_signed'], 0)

    def test_upload_document_no_file_selected(self):
        response = self.app.post('/upload_document', data={}, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file selected or invalid file name', response.data)

if __name__ == '__main__':
    unittest.main()
