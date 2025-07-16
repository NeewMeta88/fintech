from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by('owner_name')

    def perform_create(self, serializer):
        user = self.request.user
        account_count = Account.objects.filter(user=user).count()
        index = account_count + 1
        owner_name = f"{user.username}({index})"

        serializer.save(user=user, owner_name=owner_name)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.balance != 0:
            return Response({"detail": "Невозможно удалить счёт: на счёте есть деньги."},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

def account_detail_view(request, account_id):
    return render(request, 'account_detail.html', {'account_id': account_id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_accounts(request):
    if not request.user.is_superuser:
        return Response({"detail": "Для просмотра данной статистики требуется иметь права администратора."}, status=status.HTTP_403_FORBIDDEN)

    accounts = Account.objects.order_by('owner_name')
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)
