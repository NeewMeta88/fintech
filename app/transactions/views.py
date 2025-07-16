from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from app.accounts.models import Account
from app.transactions.models import Transaction
from app.transactions.serializers import TransactionSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_transactions(request):
    user_accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(
        Q(from_account__in=user_accounts) | Q(to_account__in=user_accounts)
    ).order_by('-created_at')
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@login_required
def make_transaction_page(request):
    return render(request, 'make_transaction.html')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def create_transaction_api(request):
    serializer = TransactionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
