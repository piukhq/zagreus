from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.contrib.admin import ChoicesFieldListFilter
from app.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('third_party_id', 'type', 'provider', 'time', 'amount', 'payment_card_token', 'mid', 'auth_code')
    search_fields = ('amount', 'payment_card_token', 'mid', 'auth_code')
    readonly_fields = ('type',)
    list_filter = (
        'provider',
        ('currency_code', ChoicesFieldListFilter)
    )
    advanced_filter_fields = (
        'third_party_id',
        'amount',
        'payment_card_token',
        'mid',
        'auth_code',
        'time',
    )
