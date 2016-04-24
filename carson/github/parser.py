import requests

class Parser(object):

    def get_pull_request_data(self, url):
        return requests.get(url).json()

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
