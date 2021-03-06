# -*- coding: utf-8 -*-

from __future__ import absolute_import

import mock

from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from sentry.plugins.bases.issue import IssuePlugin
from sentry.testutils import TestCase


class GetAuthForUserTest(TestCase):
    def _get_mock_user(self):
        user = mock.Mock(spec=User())
        user.id = 1
        user.is_authenticated.return_value = False
        return user

    def test_requires_auth_provider(self):
        user = self._get_mock_user()
        p = IssuePlugin()
        self.assertRaises(AssertionError, p.get_auth_for_user, user)

    def test_returns_none_on_missing_identity(self):
        user = self._get_mock_user()
        p = IssuePlugin()
        p.auth_provider = 'test'
        self.assertEquals(p.get_auth_for_user(user), None)

    def test_returns_identity(self):
        user = User.objects.create(username='test', email='test@example.com')
        auth = UserSocialAuth.objects.create(provider='test', user=user)
        p = IssuePlugin()
        p.auth_provider = 'test'
        self.assertEquals(p.get_auth_for_user(user), auth)
