import os
from unittest.mock import Mock
import unittest
import main
import auth


class HttpTest(unittest.TestCase):
    def test_return_ok(self):
        req = Mock()
        assert main.update_youtube_data(req) == 'OK'

class AuthenticationTests(unittest.TestCase):
    def test_format_env_to_secrets(self):
        auth.format_env_to_secrets()
        opened = None
        try:
            f = open("secrets.txt", "r")
            opened = True
            f.close()
            os.remove("secrets.txt")
        except FileNotFoundError:
            opened = False
        assert opened ==  True

    def test_get_client_configs(self):
        auth.format_env_to_secrets()
        configs = auth.get_client_config()
        os.remove("secrets.txt")
        assert type(configs["installed"]) == dict
        assert len(configs) != 0
        





if __name__ == '__main__':
    unittest.main()