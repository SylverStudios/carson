import unittest
import os
import json
from carson.slack.client import SlackClient

class SlackClientTest(unittest.TestCase):

    MOCK_API_KEY = "123abc"

    TEST_CONTENT = "totes content tho"

    def mock_slack_api_call(self, url, json):
        self.assertEqual(url, 'https://hooks.slack.com/services/123abc')
        self.assertEqual(json['username'], 'carson')
        self.assertEqual(json['icon_emoji'], ':robot_face:')
        self.assertEqual(json['text'], self.TEST_CONTENT)
        self.assertEqual(len(json['attachments']), 1)
        self.assertEqual(json['attachments'][0]['title'], "Pull Request #312")
        self.assertEqual(json['attachments'][0]['title_link'],
            "https://github.com/SylverStudios/carson/pull/312")
    def mock_get_slack_api_key(self):
        return self.MOCK_API_KEY

    def get_client_instance(self):
        slack_client = SlackClient()
        slack_client.slack_api_call = self.mock_slack_api_call
        slack_client.get_slack_api_key = self.mock_get_slack_api_key
        return slack_client

    def test_send_message(self):
        slack_client = self.get_client_instance()
        slack_client.send_message(
            owner="SylverStudios", repo="carson", pr_number=312, content=self.TEST_CONTENT)
