from flask_bot.app import app
import unittest


class TestRoot(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_verify_with_no_request_args(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok')
