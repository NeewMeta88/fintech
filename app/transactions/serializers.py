from django.db import transaction as db_transaction
from rest_framework import serializers

from app.kafka_app.producer import publish_transaction_event
from .models import Transaction
from ..accounts.models import Account


def create(self, validated_data):
    with db_transaction.atomic():
        from_acc = Account.objects.select_for_update().get(id=validated_data['from_account'].id)
        to_acc = Account.objects.select_for_update().get(id=validated_data['to_account'].id)
        amount = validated_data['amount']
        from_acc.balance -= amount
        to_acc.balance += amount
        from_acc.save()
        to_acc.save()
        tx = Transaction.objects.create(**validated_data)
        publish_transaction_event(tx)
        return tx


class TransactionSerializer(serializers.ModelSerializer):
    from_account_owner = serializers.CharField(source='from_account.owner_name', read_only=True)
    to_account_owner = serializers.CharField(source='to_account.owner_name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'from_account', 'to_account', 'from_account_owner', 'to_account_owner', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        from_account = data['from_account']
        to_account = data['to_account']
        amount = data['amount']

        if from_account == to_account:
            raise serializers.ValidationError("Нельзя переводить самому себе.")
        if amount <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной.")
        if from_account.balance < amount:
            raise serializers.ValidationError("Недостаточно средств на счете.")
        if request and from_account.user != request.user:
            raise serializers.ValidationError("Вы не владеете исходным счётом.")

        return data

    def create(self, validated_data):
        with db_transaction.atomic():
            from_acc = validated_data['from_account']
            to_acc = validated_data['to_account']
            amount = validated_data['amount']
            from_acc.balance -= amount
            to_acc.balance += amount
            from_acc.save()
            to_acc.save()
            return Transaction.objects.create(**validated_data)
