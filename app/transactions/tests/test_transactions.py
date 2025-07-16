
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from app.accounts.models import Account


class TransactionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass")
        self.client.login(username="user1", password="pass")
        self.a1 = Account.objects.create(user=self.user, owner_name="user1(1)", balance=1000)
        self.a2 = Account.objects.create(user=self.user, owner_name="user1(2)", balance=500)

    def test_transaction_success(self):
        response = self.client.post("/api/transactions/create/", {
            "from_account": str(self.a1.id),
            "to_account": str(self.a2.id),
            "amount": 300
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.a1.refresh_from_db()
        self.a2.refresh_from_db()
        self.assertEqual(self.a1.balance, 700)
        self.assertEqual(self.a2.balance, 800)

    def test_transaction_insufficient_funds(self):
        response = self.client.post("/api/transactions/create/", {
            "from_account": str(self.a2.id),
            "to_account": str(self.a1.id),
            "amount": 1000
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Недостаточно средств", str(response.data))

    def test_transaction_to_self(self):
        response = self.client.post("/api/transactions/create/", {
            "from_account": str(self.a1.id),
            "to_account": str(self.a1.id),
            "amount": 100
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Нельзя переводить самому себе", str(response.data))

    def test_transaction_negative_amount(self):
        response = self.client.post("/api/transactions/create/", {
            "from_account": str(self.a1.id),
            "to_account": str(self.a2.id),
            "amount": -50
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Сумма должна быть положительной", str(response.data))
