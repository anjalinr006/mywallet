from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from walletapi.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
import django.utils.timezone as tz
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class IsNotDisable(permissions.BasePermission):
    def has_permission(self, request, view, ):
        token = request.META.get("HTTP_AUTHORIZATION")
        token_obj = Token.objects.get(key=token.replace('Token ', ''))
        wallet = get_object_or_404(Wallet, owned_by=token_obj.user.username)
        return not wallet.is_disabled


class IsMakeEnable(permissions.BasePermission):
    def has_permission(self, request, view, ):
        token = request.META.get("HTTP_AUTHORIZATION")
        token_obj = Token.objects.get(key=token.replace('Token ', ''))
        wallet = get_object_or_404(Wallet, owned_by=token_obj.user.username)
        if request.method == 'POST':
            return wallet.is_disabled
        if request.method == 'GET':
            return not wallet.is_disabled
        if request.method == 'PATCH':
            return True


def getting_wallet_from_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_obj = Token.objects.get(key=token.replace('Token ', ''))
    wallet = get_object_or_404(Wallet, owned_by=token_obj.user.username)
    return wallet


@api_view(['POST'])
def create_wallet_account(request):
    if request.method == 'POST':
        customer_xid = request.data.get("customer_xid", None)
        if customer_xid:
            if User.objects.filter(username=customer_xid).exists():
                user = User.objects.get(username=customer_xid)
            else:
                user = User.objects.create(username=customer_xid)
                wallet = Wallet(owned_by=customer_xid, id=create_id(), status_last_updated=tz.localtime())
                wallet.save()

            if Token.objects.filter(user=user).exists():
                token = Token.objects.get(user=user)
            else:
                token = Token.objects.create(user=user)
            data = {
                        "status": "success",
                        "data": {'token': token.key}
                    }
            return Response(data)
        else:
            return Response({"message": "Customer Xid is not valid", "status": "fail"})


@api_view(['HEAD', 'POST', 'GET', 'PATCH'])
@permission_classes([IsAuthenticated, IsMakeEnable])
def enable_wallet_account(request):
    wallet = getting_wallet_from_token(request)
    if request.method == 'POST':
        wallet.is_disabled = False
        wallet.status_last_updated = tz.localtime()
        wallet.save()
        text = "enabled_at"
    elif request.method == 'PATCH':
        disabling_data = dict(request.data)
        disabling_data.update({'status_last_updated': tz.localtime()})
        serializer = WalletSerializer(wallet, data=disabling_data,
                                      partial=True)
        if serializer.is_valid():
            serializer.save()
        text = "disabled_at"
    else:
        text = "enabled_at"

    serializer = WalletSerializer(wallet)
    data = serializer.data
    data[text] = data.pop('status_last_updated')
    del data['is_disabled']

    val = {"status": "Success",
                "data": {
                    "wallet": data
                }
            }
    return Response(val)


@api_view(['HEAD', 'POST'])
@permission_classes([IsAuthenticated, IsNotDisable])
def wallet_transaction(request, transaction_type):
    if request.method == 'POST':
        amount = request.data.get("amount", None)
        reference_id = request.data.get("reference_id", None)
        wallet = getting_wallet_from_token(request)
        if (transaction_type == 'withdrawals') and (int(amount) > wallet.balance):
            return Response({"status": "Fail",
                             "message": "Your Blance is %d " % (wallet.balance)
                             })

        elif Transactions.objects.filter(reference_id=reference_id).exists():
            return Response({"status": "Fail",
                             "message": "This reference id is already present"
                             })

        else:

            transaction = Transactions(
                id=create_id(),
                wallet=wallet,
                type=transaction_type,
                transaction_by=wallet.owned_by,
                time=tz.localtime(),
                status="success",
                reference_id=reference_id,
                amount=amount
            )
            transaction.save()
            serializer = TransactionSerializer(transaction)
            data = serializer.data
            if transaction_type == "deposits":
                data['deposited_by'] = data.pop('transaction_by')
                data['deposited_at'] = data.pop('time')
                wallet.balance = wallet.balance + int(amount)
                transaction_data = {
                   "withdrawal": data
               }

            else:
                data['withdrawn_by'] = data.pop('transaction_by')
                data['withdrawn_at'] = data.pop('time')
                wallet.balance = wallet.balance - int(amount)
                transaction_data = {
                    "deposit": data
                }
            wallet.save()

            val = {"status": "Success",
                   "data": transaction_data}
        return Response(val)
