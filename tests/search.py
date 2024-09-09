import unittest
from unittest.mock import patch, MagicMock
from myapp import app, get_db

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('myapp.get_db')
    def test_search_post_request(self, mock_get_db):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name_doc': 'document1.pdf', 'uploaded_by': 1, 'is_signed': 0},
            {'id': 2, 'name_doc': 'document2.pdf', 'uploaded_by': 1, 'is_signed': 0}
        ]

        response = self.app.post('/search', data={'query': 'document'})

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM documents WHERE name_doc LIKE ?", ('%document%',)
        )

        self.assertIn(b'document1.pdf', response.data)
        self.assertIn(b'document2.pdf', response.data)

    @patch('myapp.get_db')
    def test_search_get_request(self, mock_get_db):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name_doc': 'document1.pdf', 'uploaded_by': 1, 'is_signed': 0},
            {'id': 2, 'name_doc': 'document2.pdf', 'uploaded_by': 1, 'is_signed': 0},
            {'id': 3, 'name_doc': 'document3.pdf', 'uploaded_by': 2, 'is_signed': 1}
        ]

        response = self.app.get('/search')

        mock_cursor.execute.assert_called_once_with("SELECT * FROM documents")

        self.assertIn(b'document1.pdf', response.data)
        self.assertIn(b'document2.pdf', response.data)
        self.assertIn(b'document3.pdf', response.data)

if __name__ == '__main__':
    unittest.main()
