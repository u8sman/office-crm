from django.contrib import admin

from unfold.admin import ModelAdmin

from crm.utils.admfilters import ScrollRelatedOnlyFieldListFilter
from voip.models import Connection


@admin.register(Connection)
class ConnectionAdmin(ModelAdmin):
    list_display = (
        "callerid",
        "provider",
        "number",
        "type",
        "owner",
        "active",
    )
    list_filter = (
        "active",
        "type",
        ("owner", ScrollRelatedOnlyFieldListFilter),
    )
    search_fields = (
        "callerid",
        "number",
        "provider__name",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
    )
    raw_id_fields = ("owner",)
    ordering = ("provider", "number")
    list_per_page = 25

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("provider", "active"),
                    ("number", "type"),
                    "callerid",
                    "owner",
                )
            },
        ),
    )
