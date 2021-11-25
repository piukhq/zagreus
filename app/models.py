from django.contrib.postgres.fields import JSONField
from django.db import models


class Transaction(models.Model):
    provider_slug = models.CharField(max_length=50, verbose_name="Provider Slug")
    payload = JSONField(verbose_name="Payload (Raw)")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return f"{self.provider_slug.title()} auth transaction"
