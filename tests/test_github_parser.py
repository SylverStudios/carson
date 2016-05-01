import unittest
import os
import json
from carson.github.parser import Parser
from carson.slack.client import SlackClient

class GithubParserTest(unittest.TestCase):

    SEND_SLACK_MESSAGE_PR_NUMBERS = []

    def mock_get_pull_request_data(self, url):
        self.assertEqual(url, 'https://api.github.com/repos/SylverStudios/carson/pulls/2')
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), 'test_github_pull_api_get.json')).read()
        )
    def mock_get_affected_prs(self, url):
        self.assertEqual(url, 'https://api.github.com/repos/SylverStudios/carson/pulls?q=is%3Apr+148b009347b2845e53a828cb3bdbde34e685e50e')
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), 'test_github_pr_query_by_commit.json')).read()
        )
    def mock_send_slack_message(self, owner, repo, pr_number, content):
        self.assertEqual(owner, 'SylverStudios')
        self.assertEqual(repo, 'carson')
        self.assertEqual(content, 'A test failed!')
        self.SEND_SLACK_MESSAGE_PR_NUMBERS.append(pr_number)

    def get_slack_client(self):
        slack_client = SlackClient()
        slack_client.send_message = self.mock_send_slack_message
        return slack_client
    def get_parser_instance(self):
        parser = Parser()
        parser.get_pull_request_data = self.mock_get_pull_request_data
        parser.get_affected_prs = self.mock_get_affected_prs
        parser.get_slack_client = self.get_slack_client
        return parser

    def get_test_comment_event(self):
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), 'test_github_comment_event.json')).read()
        )
    def get_test_commit_status_failure(self):
        return json.loads(
            open(os.path.join(os.path.dirname(__file__), 'test_github_commit_status_message_failure.json')).read()
        )

    def assert_parsed_data(self, parsed_data):
        self.assertEqual(parsed_data['commit_sha'], '7753bb8a60c85105636aaa176c830475b3fa1586')
        self.assertEqual(parsed_data['gh_username'], 'samgqroberts')
        self.assertEqual(parsed_data['timestamp'], '2016-04-24T17:40:32Z')
        self.assertEqual(parsed_data['pr_number'], 2)
        self.assertEqual(parsed_data['repo'], 'SylverStudios/carson')
        self.assertEqual(parsed_data['base_branch'], 'master')

    def test_parse_comment_matp(self):
        comment_data = self.get_test_comment_event()
        comment_data['comment']['body'] = 'blah blah carson matp blah blah'
        parser = self.get_parser_instance()
        parsed_data = parser.parse_comment_message(comment_data)
        self.assert_parsed_data(parsed_data)
        condition_action_pairings = parsed_data['condition_action_pairings']
        self.assertEqual(len(condition_action_pairings), 1)
        pairing = condition_action_pairings[0]
        self.assertEqual(pairing['condition'], 'passed')
        self.assertIn('merge', pairing['actions'])
        self.assertIn('notify_slack', pairing['actions'])

    def test_parse_comment_no_message_encoded(self):
        comment_data = self.get_test_comment_event()
        comment_data['comment']['body'] = 'blah blah blah blah'
        parser = self.get_parser_instance()
        parsed_data = parser.parse_comment_message(comment_data)
        self.assert_parsed_data(parsed_data)
        condition_action_pairings = parsed_data['condition_action_pairings']
        self.assertEqual(len(condition_action_pairings), 0)

    def test_parse_commit_status_failure(self):
        commit_status = self.get_test_commit_status_failure()
        parser = self.get_parser_instance()
        parser.parse_commit_status(commit_status)
        self.assertIn(4, self.SEND_SLACK_MESSAGE_PR_NUMBERS)
        self.assertIn(6, self.SEND_SLACK_MESSAGE_PR_NUMBERS)
