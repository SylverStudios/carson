import requests
from .. import app


class NotifyAction(object):
    URL = "https://hooks.slack.com/services/{key}"
    PR_URL = "https://github.com/{r}/pull/{pr}"

    PASS_MESSAGE = "All tests passed on PR #{pr}"
    FAIL_MESSAGE = "One or more tests failed on PR #{pr}"
    MERGING_MESSAGE = "Merging PR #{pr}"

    def __init__(self, appointment, message=None):
        self.appointment = appointment
        self.message = message
        self.key = app.config.get("SLACK_API_KEY")

    def __msg(self, msg):
        return msg.format(pr=self.appointment.pr_number)

    def __pr_link(self):
        return self.PR_URL.format(
            pr=self.appointment.pr_number, r=self.appointment.repo)

    def __msg_from_appointment(self):
        if self.message is not None:
            return self.message
        if self.appointment.conditions == "any_failed":
            return self.__msg(self.FAIL_MESSAGE)
        # all_passed
        if self.appointment.action == "merge":
            return self.__msg(self.MERGING_MESSAGE)
        return self.__msg(self.PASS_MESSAGE)

    def get_users(self):
        return ["#carson"]  # TODO

    def run(self):
        message = self.__msg_from_appointment()
        url = self.URL.format(key=self.key)
        data = {
            "username": "carson",
            "icon_emoji": ":robot_face:",
            "text": message,
            "attachments": [{
                "title": "Pull Request #{}".format(self.appointment.pr_number),
                "title_link": self.__pr_link()
            }]
        }
        for user in self.get_users():
            data['channel'] = user
            requests.post(url, json=data)
