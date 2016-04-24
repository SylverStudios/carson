import requests

from .auth import UrlBuilder


class MergeAction(object):
    """Action that merges a pull request via the SHA of its head commit
    See: https://developer.github.com/v3/repos/merging/
    """
    URL = "/repos/{fullname}/merges"

    def __init__(self, appointment):
        self.appointment = appointment

    def run(self):
        resource = self.URL.format(fullname=self.appointment.repo)
        url = UrlBuilder(resource).get()
        data = {
            "base": self.appointment.base_branch,
            "head": self.appointment.commit_sha,
        }
        resp = requests.post(url, json=data)
        self.status = resp.status_code

    def get_message(self):
        return "Merge status for PR #{pr}: {m}".format(
            pr=self.appointment.pr_number,
            m=self.__message_from_status())

    def __message_from_status(self):
        if self.status == 201:
            return "Merge completed successfully"
        elif self.status == 204:
            return "Base already contains head commit, nothing to merge"
        elif self.status == 409:
            return "Hit merge conflict, could not merge"
        elif self.status == 404:
            return "Base or head do not exist"
