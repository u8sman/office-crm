from django.contrib import admin
from unfold.admin import ModelAdmin

from chat.models import ChatMessage
from chat.site import chatmessageadmin
from crm.site.crmadminsite import crm_site


class ChatMessageAdmin(ModelAdmin):
    list_display = (
        'content',
        'owner',
        'creation_date',
        'id'
    )
    raw_id_fields = ('topic', 'answer_to')
    search_fields = ('content',)


admin.site.register(ChatMessage, ChatMessageAdmin)

crm_site.register(ChatMessage, chatmessageadmin.ChatMessageAdmin)
