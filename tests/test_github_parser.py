import unittest
import os
import json
from carson.github.parser import Parser

class GithubParserTest(unittest.TestCase):

    def mock_get_pull_request_data(self, url):
        self.assertEqual(url, 'https://api.github.com/repos/SylverStudios/carson/pulls/2')
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), 'test_github_pull_api_get.json')).read()
        )

    def test_hello(self):
        json_data=open(os.path.join(os.path.dirname(__file__), 'test_github_comment_event.json')).read()
        data = json.loads(json_data)
        parser = Parser()
        parser.get_pull_request_data = self.mock_get_pull_request_data
        parsedData = parser.parse_comment_message(data)
        self.assertEqual(parsedData['sha'], 'a5b6485a079091efbe6d5aa5122acec1dde02df4')
        self.assertEqual(parsedData['github_username'], 'samgqroberts')
        self.assertEqual(parsedData['timestamp'], '2016-04-24T17:40:32Z')
        self.assertEqual(parsedData['issue_number'], 2)
        self.assertEqual(parsedData['repo'], 'SylverStudios/carson')
        self.assertEqual(parsedData['base_branch'], 'master')
