from django.db import models
import uuid


TRANSACTION_TYPES = (('withdrawals', 'withdrawals'),
                    ('deposits', 'deposits'))

TRANSACTION_STATUS = (('success', 'success'),
                      ('failed', 'failed'),
                      ('pending', 'pending'))


def create_id():
    uuid_list = [uuid.uuid4().hex[:8].lower(), uuid.uuid4().hex[:4].lower(), uuid.uuid4().hex[:4].lower(),
                 uuid.uuid4().hex[:12].lower()]
    joined_string = "-".join(uuid_list)
    return joined_string


class Wallet(models.Model):
    id = models.CharField(unique=True, max_length=100, primary_key=True, default=create_id(), verbose_name='id')
    owned_by = models.CharField(unique=True, max_length=100,  verbose_name='Owned By')
    is_disabled = models.BooleanField(default=True)
    status_last_updated = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    balance = models.DecimalField(max_digits=22, decimal_places=4, default=0)


class Transactions(models.Model):
    id = models.CharField(unique=True, max_length=100, default=create_id(), primary_key=True, verbose_name='id')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=100000, choices=TRANSACTION_TYPES)
    transaction_by = models.CharField(max_length=100000, verbose_name='Transaction By')
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100000, choices=TRANSACTION_STATUS)
    reference_id = models.CharField(max_length=100000, unique=True, verbose_name='Referance Id')
    amount = models.DecimalField(max_digits=22, decimal_places=4, default=0)


