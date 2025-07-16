from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owner_name', 'balance', 'created_at']
        read_only_fields = ['id', 'owner_name', 'created_at', 'balance']