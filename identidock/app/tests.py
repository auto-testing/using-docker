# http://flask.pocoo.org/docs/1.0/tutorial/tests/
import unittest
import identidock

class TestCase( unittest.TestCase):

    def setUp(self):
        identidock.app.config['TESTING'] = True # http://flask.pocoo.org/docs/1.0/config/#TESTING
        self.test_client = identidock.app.test_client()
        
    def test_get_mainpage(self):
        page = self.test_client.post("/", data={'name':"Moby Dick"})
        assert page.status_code == 200
        assert 'Hello' in str(page.data)
        assert "Moby Dick" in str(page.data)
    
    def test_html_escaping(self):
        page = self.test_client.post("/", data={'name':'"><b>TEST</b><!---'})
        assert '<b>' not in str(page.data)
        
if __name__ == '__main__':
    unittest.main()