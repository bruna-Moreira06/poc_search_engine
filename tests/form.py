import unittest
from flask import Flask, render_template_string
from flask_testing import TestCase

class TestSearchPage(TestCase):
    def create_app(self):
        return app

    def test_page_elements(self):
        response = self.client.get('/search')
        self.assert200(response)
        
        self.assertIn(b'Search Documents', response.data)
        self.assertIn(b'Enter search query', response.data)
        self.assertIn(b'Search', response.data)
        self.assertIn(b'Reset', response.data)
        self.assertIn(b'Back to Home', response.data)
        
        self.assertIn(b'<form method="post">', response.data)
        self.assertIn(b'<input type="text" name="query"', response.data)
        self.assertIn(b'<input type="submit" value="Search"', response.data)
        self.assertIn(b'<input type="button" value="Reset"', response.data)
        
        self.assertIn(b'<h2>Uploaded Documents</h2>', response.data)

if __name__ == '__main__':
    unittest.main()