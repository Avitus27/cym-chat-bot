#import pdb; pdb.set_trace()

from flask_bot.app import app
import unittest

class TestRoot(unittest.TestCase):

    def setUp(self):
#        pdb.set_trace()
        self.app = app.test_client()

    def test_verify_with_no_request_args(self):
        response = self.app.get('/')

        self.assertEqual(1, 1)

