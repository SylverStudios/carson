
class NotifyAction(object):
    PASS_MESSAGE = "All tests passed on PR #{pr}"
    FAIL_MESSAGE = "One or more tests failed on PR #{pr}"
    MERGING_MESSAGE = "Merging PR #{pr}"

    def __init__(self, appointment, message=None):
        self.appointment = appointment
        self.message = message

    def run(self):
        pass  # TODO :-)
