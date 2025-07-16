
from django.db import migrations
from django.utils.timezone import datetime


def add_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Account = apps.get_model('accounts', 'Account')
    Transaction = apps.get_model('transactions', 'Transaction')

    if not User.objects.filter(username='admin').exists():
        user1 = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
    else:
        user1 = User.objects.get(username='admin')

    if not User.objects.filter(username='test').exists():
        user2 = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test'
        )
    else:
        user2 = User.objects.get(username='user2')

    account1 = Account.objects.create(
        user=user1,
        owner_name='admin(1)',
        balance=60
    )

    account2 = Account.objects.create(
        user=user1,
        owner_name='admin(2)',
        balance=20
    )

    account3 = Account.objects.create(
        user=user1,
        owner_name='admin(3)',
        balance=10
    )

    account4 = Account.objects.create(
        user=user2,
        owner_name='test(1)',
        balance=10
    )

    Transaction.objects.create(
        from_account=account1,
        to_account=account2,
        amount=10,
        created_at=datetime(2025, 7, 16, 16, 30)
    )

    Transaction.objects.create(
        from_account=account1,
        to_account=account3,
        amount=5,
        created_at=datetime(2025, 7, 16, 16, 40)
    )

    Transaction.objects.create(
        from_account=account4,
        to_account=account2,
        amount=7,
        created_at=datetime(2025, 7, 16, 16, 45)
    )


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]
