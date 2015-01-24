from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import User


class AccountsModelsTestCase(TestCase):
    def test_user_is_auth_user_model(self):
        self.assertEqual(get_user_model(), User)
