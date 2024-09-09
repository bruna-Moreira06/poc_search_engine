import unittest
from unittest.mock import patch, MagicMock
from myapp import delete_document, get_db

class DeleteDocumentTestCase(unittest.TestCase):
    @patch('myapp.es.delete')
    @patch('myapp.get_db')
    def test_delete_document_success(self, mock_get_db, mock_es_delete):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        document_id = 123

        delete_document(document_id)

        mock_cursor.execute.assert_called_once_with("DELETE FROM documents WHERE id = ?", (document_id,))
        mock_db.commit.assert_called_once()

        mock_es_delete.assert_called_once_with(index="documents", id=document_id)

    @patch('myapp.es.delete')
    @patch('myapp.get_db')
    def test_delete_document_elasticsearch_failure(self, mock_get_db, mock_es_delete):
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_es_delete.side_effect = Exception("Elasticsearch deletion failed")

        document_id = 123

        with self.assertLogs(level='ERROR') as log:
            delete_document(document_id)

            mock_cursor.execute.assert_called_once_with("DELETE FROM documents WHERE id = ?", (document_id,))
            mock_db.commit.assert_called_once()

            mock_es_delete.assert_called_once_with(index="documents", id=document_id)

            self.assertIn("Elasticsearch deletion failed", log.output[0])

if __name__ == '__main__':
    unittest.main()
