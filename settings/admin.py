from django.contrib import admin
from django.http import HttpResponseRedirect

from unfold.admin import ModelAdmin

from crm.site.crmadminsite import crm_site
from settings.models import (
    BannedCompanyName,
    MassmailSettings,
    PublicEmailDomain,
    Reminders,
    StopPhrase,
)


@admin.register(BannedCompanyName)
class BannedCompanyNameAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25


@admin.register(MassmailSettings)
class MassmailSettingsAdmin(ModelAdmin):
    """
    Singleton-style settings model. Unfold-styled form with
    read-only changelist that redirects to the single instance.
    """

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "emails_per_day",
                    "use_business_time",
                    "business_time_start",
                    "business_time_end",
                    "unsubscribe_url",
                )
            },
        ),
    )

    # -- ModelAdmin methods -- #

    def changelist_view(self, request, extra_context=None):
        # Always redirect list view to the single object with pk=1
        return HttpResponseRedirect(f"{request.path}1/change/")

    def has_add_permission(self, request):
        # Prevent creating new instances – singleton
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the singleton
        return False


@admin.register(PublicEmailDomain)
class PublicEmailDomainAdmin(ModelAdmin):
    list_display = ("domain",)
    search_fields = ("domain",)
    ordering = ("domain",)
    list_per_page = 25


@admin.register(Reminders)
class RemindersAdmin(ModelAdmin):
    """
    Singleton-style reminders settings.
    """

    # -- ModelAdmin methods -- #

    def changelist_view(self, request, extra_context=None):
        # Always redirect list view to the single object with pk=1
        return HttpResponseRedirect(f"{request.path}1/change/")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StopPhrase)
class StopPhraseAdmin(ModelAdmin):
    actions = ["delete_selected"]
    list_display = ("phrase", "last_occurrence_date")
    search_fields = ("phrase",)
    ordering = ("phrase",)
    list_per_page = 25


# --- CRM custom admin site registrations (unchanged) --- #

crm_site.register(BannedCompanyName, BannedCompanyNameAdmin)
crm_site.register(PublicEmailDomain, PublicEmailDomainAdmin)
crm_site.register(StopPhrase, StopPhraseAdmin)
