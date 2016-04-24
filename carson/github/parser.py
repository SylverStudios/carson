class Parser(object):
    def parse(self, message):
        parsed = {
          'issue_number': message['issue']['number']
        }
        return parsed
