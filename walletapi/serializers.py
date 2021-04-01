from rest_framework import serializers
from walletapi.models import *


class WalletSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('id', 'owned_by', 'status', 'is_disabled', 'status_last_updated', 'balance')

    def get_status(self, obj):
        if obj.is_disabled:
            return 'disabled'
        else:
            return 'enabled'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('id', 'transaction_by', 'status', 'time', 'amount', 'reference_id')



