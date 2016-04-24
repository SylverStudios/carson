import unittest
import os
import json
from carson.github.parser import Parser

class GithubParserTest(unittest.TestCase):
    def test_hello(self):
        json_data=open(os.path.join(os.path.dirname(__file__), 'test_github_message.json')).read()
        data = json.loads(json_data)
        parsedData = Parser().parse(data)
        self.assertEqual(parsedData['issue_number'], 2)
