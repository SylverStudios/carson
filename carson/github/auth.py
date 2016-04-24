from .. import app


class UrlBuilder(object):
    BASE = "https://api.github.com"
    TOKEN_PARAM = "access_token"

    def __init__(self, resource):
        self.resource = resource

    def get(self):
        return "{b}{r}?{tp}={a}".format(
            b=self.BASE, r=self.resource,
            tp=self.TOKEN_PARAM, a=app.config.get('GITHUB_API_KEY')
        )
