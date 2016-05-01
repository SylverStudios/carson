import requests
from ..slack.client import SlackClient

class Parser(object):
    PR_QUERY_BY_COMMIT_URL = "https://api.github.com/repos/{owner}/{repo}/pulls?q=is%3Apr+{sha}"

    # wrapped for testing
    def get_pull_request_data(self, url):
        return requests.get(url).json()
    def get_affected_prs(self, url):
        return requests.get(url).json()
    def get_slack_client(self):
        return SlackClient()

    def discern_condition_and_actions(self, comment_body):
        condition_action_pairings = [];
        if "carson matp" in comment_body:
            condition_action_pairings.append({
                'condition': 'passed',
                'actions': ['merge', 'notify_slack'],
            })
        return condition_action_pairings

    def parse_comment_message(self, comment_message):
        # need to get pull request information to (another API call)
        pull_request_api_url = comment_message['issue']['pull_request']['url']
        pull_request_data = self.get_pull_request_data(pull_request_api_url)
        # parse comment body for event information
        comment_body = comment_message['comment']['body']
        # compile and return relevant information
        parsed = {
            'commit_sha': pull_request_data['head']['sha'],
            'gh_username': comment_message['sender']['login'],
            'timestamp': comment_message['comment']['created_at'],
            'pr_number': comment_message['issue']['number'],
            'repo': comment_message['repository']['full_name'],
            'base_branch': pull_request_data['base']['ref'],
            'condition_action_pairings': self.discern_condition_and_actions(comment_body),
        }
        return parsed

    def parse_commit_status(self, commit_status):
        if commit_status['state'] == 'failure':
            owner = commit_status['repository']['owner']['login']
            repo = commit_status['repository']['name']
            sha = commit_status['sha']
            affected_prs_query_url = self.PR_QUERY_BY_COMMIT_URL.format(
                owner=owner, repo=repo, sha=sha)
            affected_prs = self.get_affected_prs(affected_prs_query_url)
            for affected_pr in affected_prs:
                print(affected_pr['number'])
                self.get_slack_client().send_message(owner=owner, repo=repo,
                    pr_number=affected_pr['number'], content="A test failed!")
