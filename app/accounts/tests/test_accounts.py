from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from app.accounts.models import Account


class AccountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass")
        self.client.login(username="user1", password="pass")
        self.a1 = Account.objects.create(user=self.user, owner_name="user1(1)", balance=1000)
        self.a2 = Account.objects.create(user=self.user, owner_name="user1(2)", balance=500)

    def test_create_account(self):
        account = Account.objects.create(user=self.user, owner_name="new", balance=0)
        self.assertEqual(account.owner_name, "new")
        self.assertEqual(account.balance, 0)

    def test_get_account_list(self):
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_account_detail(self):
        response = self.client.get(f"/api/accounts/{self.a1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.a1.id))
