from unittest.mock import patch
from django.test import SimpleTestCase
from decouple import RepositoryEnv, config as decouple_config

from core.env import get_config


class TestEnv(SimpleTestCase):
    @patch("core.env.ENV_FILE")
    def test_envfile(self, patched_env):
        patched_env.exists.return_value = True
        config = get_config()
        self.assertTrue(isinstance(config.repository, RepositoryEnv))

    @patch("core.env.ENV_FILE")
    def test_no_envfile(self, patched_env):
        patched_env.exists.return_value = False
        get_config.cache_clear()
        config = get_config()
        self.assertEqual(config, decouple_config)
