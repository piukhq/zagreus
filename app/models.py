from django.db import models


class Transaction(models.Model):
    CURRENCIES = (
        ('GBP', 'pound sterling'),
        ('USD', 'US dollar'),
        ('EUR', 'euro')
    )

    time = models.DateTimeField()
    auth_code = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField()
    payment_card_token = models.CharField(max_length=255)
    mid = models.CharField(max_length=255)
    third_party_id = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=5, choices=CURRENCIES)
    provider = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)

    @property
    def type(self):
        if self.auth_code:
            return 'AUTH'
        return 'SETTLED'

    def __str__(self):
        return f'{self.provider}: {self.third_party_id}'
