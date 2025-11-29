from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin

from crm.site.crmmodeladmin import CrmModelAdmin
from crm.site.crmadminsite import crm_site
from massmail.models import (
    EmailAccount,
    EmlMessage,
    EmlAccountsQueue,
    MailingOut,
    MassContact,
    Signature,
)
from massmail.site import (
    emailaccountadmin,
    emlmessageadmin,
    mailingoutadmin,
    signatureadmin,
)


@admin.register(EmailAccount)
class EmailAccountAdmin(emailaccountadmin.EmailAccountAdmin):
    """
    Email account admin in the default site, extending the project-specific
    EmailAccountAdmin but giving it an explicit Unfold-styled field layout.
    """

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "main",
                    "massmail",
                    "do_import",
                    "email_host",
                    "imap_host",
                    "email_host_user",
                    "email_host_password",
                    "email_app_password",
                    "email_port",
                    "from_email",
                    "email_use_tls",
                    "email_use_ssl",
                    "email_imail_ssl_certfile",
                    "email_imail_ssl_keyfile",
                    "refresh_token",
                )
            },
        ),
        (
            _("Service information"),
            {
                "fields": (
                    "report",
                    "today_date",
                    "today_count",
                    "start_incoming_uid",
                    "start_sent_uid",
                    "last_import_dt",
                )
            },
        ),
        (
            _("Additional information"),
            {
                "fields": (
                    ("owner", "co_owner", "modified_by"),
                    ("creation_date", "update_date"),
                )
            },
        ),
    )


@admin.register(EmlMessage)
class MessageAdmin(emlmessageadmin.EmlMessageAdmin):
    """
    EmlMessage admin in the default site.
    """

    readonly_fields = (
        "modified_by",
        "signature_preview",
        "msg_preview",
    )

    # -- ModelAdmin methods -- #

    def get_form(self, request, obj=None, **kwargs):
        """
        Strip JS media from the parent form (keeps your original logic).
        """
        form = super().get_form(request, obj, **kwargs)
        form.media = forms.Media(js=[])
        return form


@admin.register(Signature)
class SignatureAdmin(signatureadmin.SignatureAdmin):
    """
    Signature admin in the default site.
    """

    readonly_fields = (
        "modified_by",
        "update_date",
        "creation_date",
        "preview",
    )


@admin.register(MailingOut)
class MailingOutAdmin(mailingoutadmin.MailingOutAdmin):
    """
    MailingOut admin in the default site, with explicit Unfold-style fieldsets.
    """

    exclude = []
    readonly_fields = list()  # you can add ('recipients_number',) back here if needed

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "status"),
                    ("content_type", "recipients_number"),
                    "message",
                    "report",
                    "recipient_ids",
                    "successful_ids",
                    "failed_ids",
                    ("owner", "modified_by"),
                )
            },
        ),
    )


@admin.register(MassContact)
class MassContactAdmin(CrmModelAdmin):
    """
    Admin for MassContact, based on project CrmModelAdmin so it inherits
    all CRM-specific behavior but still looks like Unfold.
    """

    list_display = (
        "content_object",
        "content_type",
        "object_id",
        "email_account",
        "massmail",
    )
    list_filter = (
        ("email_account__owner", admin.RelatedOnlyFieldListFilter),
        "massmail",
        ("content_type", admin.RelatedOnlyFieldListFilter),
        ("email_account", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ["object_id"]
    save_on_top = False

    # -- ModelAdmin methods -- #

    def get_list_filter(self, request):
        return self.list_filter

    def get_queryset(self, request):
        # Use the CrmModelAdmin / ModelAdmin get_queryset properly
        return super().get_queryset(request)


@admin.register(EmlAccountsQueue)
class EmlAccountsQueueAdmin(ModelAdmin):
    """
    Simple Unfold ModelAdmin for EmlAccountsQueue so it also gets the theme.
    """

    # No custom options; Unfold will still style the change list / forms.
    pass


# --- CRM custom admin site registrations (unchanged) --- #

crm_site.register(EmailAccount, emailaccountadmin.EmailAccountAdmin)
crm_site.register(EmlMessage, emlmessageadmin.EmlMessageAdmin)
crm_site.register(MailingOut, mailingoutadmin.MailingOutAdmin)
crm_site.register(Signature, signatureadmin.SignatureAdmin)
