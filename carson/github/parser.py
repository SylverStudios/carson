import requests

class Parser(object):

    def get_pull_request_data(self, url):
        return requests.get(url).json()

    def parse_comment_message(self, comment_message):
        pull_request_api_url = comment_message['issue']['pull_request']['url']
        pull_request_data = self.get_pull_request_data(pull_request_api_url)
        parsed = {
            'sha': pull_request_data['merge_commit_sha'],
            'github_username': comment_message['sender']['login'],
            'timestamp': comment_message['comment']['created_at'],
            'issue_number': comment_message['issue']['number'],
            'repo': comment_message['repository']['full_name'],
            'base_branch': pull_request_data['base']['ref'],
        }
        return parsed
