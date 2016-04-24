import unittest

from carson.github.auth import UrlBuilder
from carson import app


class AuthUrlBuilderTest(unittest.TestCase):
    def setUp(self):
        app.config = {'GITHUB_API_KEY': 'test-api-key'}

    def test_url_builder(self):
        builder = UrlBuilder("/test/resource")
        self.assertEquals(
            builder.get(),
            "https://api.github.com/test/resource?access_token=test-api-key")
