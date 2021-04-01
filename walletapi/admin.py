from django.contrib import admin
from walletapi.models import *


class TransactionAdmin(admin.TabularInline):
    model = Transactions
    readonly_fields = ['time']
    extra = 0


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_disabled', 'status_last_updated', 'balance']
    list_per_page = 20
    list_filter = ["is_disabled"]
    inlines = [TransactionAdmin]


admin.site.register(Wallet, WalletAdmin)

