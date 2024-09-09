import os
import unittest
from unittest.mock import patch, MagicMock
import fitz 
from myapp import process_pdf 

class ProcessPDFTestCase(unittest.TestCase):
    @patch('myapp.es')
    @patch('myapp.fitz.open')
    def test_process_pdf_success(self, mock_fitz_open, mock_es_index):
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample text from PDF."
        mock_doc.__iter__.return_value = [mock_page]

        mock_fitz_open.return_value = mock_doc

        pdf_path = "/fake/path/to/document.pdf"
        process_pdf(pdf_path)

        mock_fitz_open.assert_called_once_with(pdf_path)

        self.assertEqual(mock_page.get_text.call_count, len([mock_page]))

        expected_doc_data = {
            "file_name": os.path.basename(pdf_path),
            "content": "Sample text from PDF.",
            "is_signed": False
        }
        mock_es_index.index.assert_called_once_with(index="documents", body=expected_doc_data)

    @patch('myapp.fitz.open')
    def test_process_pdf_empty_document(self, mock_fitz_open):
        mock_doc = MagicMock()
        mock_doc.__iter__.return_value = []

        mock_fitz_open.return_value = mock_doc

        pdf_path = "/fake/path/to/empty_document.pdf"
        with patch('myapp.es.index') as mock_es_index:
            process_pdf(pdf_path)

            expected_doc_data = {
                "file_name": os.path.basename(pdf_path),
                "content": "",
                "is_signed": False
            }
            mock_es_index.assert_called_once_with(index="documents", body=expected_doc_data)

if __name__ == '__main__':
    unittest.main()
