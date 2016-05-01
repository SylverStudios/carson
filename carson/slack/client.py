import requests
from .. import app


class SlackClient(object):
    SLACK_URL = "https://hooks.slack.com/services/{key}"
    PR_URL = "https://github.com/{owner}/{repo}/pull/{pr_number}"

    PR_MESSAGE_TITLE = "Pull Request #{}"

    # wrapped for testing
    def slack_api_call(self, url, json):
        return requests.post(url, json)
    def get_slack_api_key(self):
        return app.config.get("SLACK_API_KEY")

    def get_users(self):
        return ["#carson"]  # TODO

    def send_message(self, owner, repo, pr_number, content):
        title = self.PR_MESSAGE_TITLE.format(pr_number)
        pr_link = self.PR_URL.format(owner=owner, repo=repo, pr_number=pr_number)
        slack_url = self.SLACK_URL.format(key=self.get_slack_api_key())
        data = {
            "username": "carson",
            "icon_emoji": ":robot_face:",
            "text": content,
            "attachments": [{
                "title": title,
                "title_link": pr_link
            }]
        }
        for user in self.get_users():
            data['channel'] = user
            self.slack_api_call(url=slack_url, json=data)
