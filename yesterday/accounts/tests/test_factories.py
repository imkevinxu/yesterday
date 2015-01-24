from django.test import TestCase
from django.contrib.auth import get_user_model

from ..factories import UserFactory, AdminUserFactory


class AccountsFactoriesTestCase(TestCase):
    def setUp(self):
        get_user_model().objects.all().delete()

    def test_user_factory(self):
        user = UserFactory(email='test@example.com')
        user_from_db = get_user_model().objects.get(email='test@example.com')
        self.assertEqual(user, user_from_db)

    def test_admin_user_factory(self):
        admin = AdminUserFactory(email='test@example.com')
        admin_from_db = get_user_model().objects.get(email='test@example.com')
        self.assertEqual(admin, admin_from_db)
        self.assertTrue(admin.is_superuser)

    def test_multiple_users_factory(self):
        users = []
        for i in range(10):
            users.append(UserFactory())
            users.append(AdminUserFactory())

        self.assertEqual(len(users), 20)
        self.assertEqual(len(users), len(get_user_model().objects.all()))
        self.assertEqual(len(get_user_model().objects.filter(is_superuser=True)), 10)
