import unittest
import requests

class TestJWKS(unittest.TestCase):
    def test_jwks(self):
        response = requests.get('http://localhost:8080/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('keys', response.json())

    def test_auth(self):
        response = requests.post('http://localhost:8080/auth')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_expired_auth(self):
        response = requests.post('http://localhost:8080/auth?expired=true')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

if __name__ == '__main__':
    unittest.main()
