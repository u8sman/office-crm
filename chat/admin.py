from django.contrib import admin
from unfold.admin import ModelAdmin

from chat.models import ChatMessage
from chat.site.chatmessageadmin import ChatMessageAdmin as CRMChatMessageAdmin
from crm.site.crmadminsite import crm_site


@admin.register(ChatMessage)
class ChatMessageAdmin(ModelAdmin):
    """
    Unfold-styled admin for ChatMessage.
    Matching consistent display, search, and performance optimizations.
    """

    list_display = (
        "content",
        "owner",
        "creation_date",
        "id",
    )
    list_display_links = ("id", "content")
    search_fields = (
        "content",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
    )
    raw_id_fields = ("topic", "answer_to")
    list_select_related = ("owner",)
    ordering = ("-creation_date",)
    list_per_page = 25
    date_hierarchy = "creation_date"


# Register in CRM custom admin site
crm_site.register(ChatMessage, CRMChatMessageAdmin)
