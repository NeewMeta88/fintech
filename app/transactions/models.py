from django.db import models
import uuid
from app.accounts.models import Account

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_account} -> {self.to_account} : {self.amount}"