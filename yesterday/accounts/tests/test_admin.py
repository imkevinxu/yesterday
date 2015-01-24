from django.test import TestCase
from django.contrib import admin
from django.contrib.auth.models import Group

from ..models import User


class AccountsAdminTestCase(TestCase):
    def test_user_in_admin(self):
        self.assertTrue(User in admin.site._registry)

    def test_group_not_in_admin(self):
        self.assertFalse(Group in admin.site._registry)
