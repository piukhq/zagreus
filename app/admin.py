import json

import pygments
import pygments.formatters
import pygments.lexers
from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("provider_slug", "created_date", "updated_date")
    list_filter = ("provider_slug",)
    fields = ("provider_slug", "created_date", "updated_date", "formatted_payload", "payload")
    readonly_fields = ("created_date", "updated_date", "formatted_payload")

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ("provider_slug", "payload")
        return self.readonly_fields

    def formatted_payload(self, instance):
        payload = json.dumps(instance.payload, sort_keys=True, indent=4)
        formatter = pygments.formatters.HtmlFormatter()
        lexer = pygments.lexers.JsonLexer()
        payload = pygments.highlight(payload, lexer, formatter)
        style = f"<style>{formatter.get_style_defs()}</style>"
        return mark_safe(style + payload)

    formatted_payload.short_description = "Payload (Formatted)"
