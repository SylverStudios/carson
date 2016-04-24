import datetime

from .models import Appointment
from .github import actions as gh
from .slack import actions as slack


class Lifecycle(object):
    """Responsible for creating/retrieving appointment objects in the DB
    given identifying info."""
    def __init__(self, gh_username, repo, sha, pr_number, base_branch):
        self.gh_username = gh_username
        self.repo = repo
        self.sha = sha
        self.pr_number = pr_number
        self.base_branch = base_branch

    def __find(self, action, conditions):
        return self.__find_or_create(action, conditions, create=False)

    def __find_or_create(self, action, conditions, create=True):
        match = Appointment.query.filter_by(
            gh_username=self.gh_username,
            repo=self.repo,
            commit_sha=self.sha,
            pr_number=self.pr_number,
            base_branch=self.base_branch,
            action=action,
            conditions=conditions,
            processed=None,
        ).one_or_none()
        if match is None and create:
            match = Appointment()
            match.repo = self.repo
            match.commit_sha = self.sha
            match.pr_number = self.pr_number
            match.gh_username = self.gh_username
            match.base_branch = self.base_branch
            match.action = action
            match.conditions = conditions
            match.write()
        return match

    def __mark_processed(self, appointment):
        appointment.processed = datetime.datetime.utcnow()
        appointment.write()

    def queue_merge(self):
        self.__find_or_create(action="merge", conditions="passed")

    def queue_notifications(self):
        self.__find_or_create(action="notify_slack", conditions="passed")
        self.__find_or_create(action="notify_slack", conditions="any_failed")

    def all_tests_passed(self):
        notify = self.__find(action="notify_slack", conditions="passed")
        if notify is not None:
            slack.NotifyAction(notify).run()
            self.__mark_processed(notify)
        merge = self.__find(action="merge", conditions="passed")
        if merge is not None:
            merge_action = gh.MergeAction(merge)
            merge_action.run()
            message = merge_action.get_message()
            slack.NotifyAction(merge, message=message).run()
            self.__mark_processed(merge)

    def any_test_failed(self):
        notify = self.__find(action="notify_slack", conditions="any_failed")
        if notify is not None:
            slack.NotifyAction(notify).run()
            self.__mark_processed(notify)
