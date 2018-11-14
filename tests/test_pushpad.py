# -*- coding: utf-8 -*-
import unittest
import pushpad


class TestPushpad(unittest.TestCase):
    _test_token = '5374d7dfeffa2eb49965624ba7596a09'
    _test_project_id = 123

    def test_instantiate(self):
        """ pushpad can be instantiated"""

        project = pushpad.Pushpad(self._test_token, self._test_project_id)
        self.assertIsNotNone(project)

    def test_set_token(self):
        """ can change auth_token """
        project = pushpad.Pushpad(self._test_token, self._test_project_id)
        self.assertEqual(project.auth_token, self._test_token)

    def test_set_project(self):
        """ can change project_id """

        project = pushpad.Pushpad(self._test_token, self._test_project_id)
        self.assertEqual(project.project_id, self._test_project_id)

    def test_get_signature(self):
        data = "Lorem ipsum dolor sit amet, cu eam veniam verear blandit"
        data_sha1 = "71b88a1cab4fa14794128debecae12f5c091f7fe"

        project = pushpad.Pushpad(self._test_token, self._test_project_id)
        self.assertEqual(project.signature_for(data), data_sha1)
