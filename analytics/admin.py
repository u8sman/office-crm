from django.contrib import admin
from django.contrib.auth.models import Permission

from unfold.admin import ModelAdmin

from analytics.models import (
    ClosingReasonStat,
    ConversionStat,
    DealStat,
    IncomeStat,
    IncomeStatSnapshot,
    LeadSourceStat,
    OutputStat,
    RequestStat,
    SalesFunnel,
)

from analytics.site.conversionadmin import ConversionStatAdmin
from analytics.site.closingreasonstatadmin import ClosingReasonStatAdmin
from analytics.site.dealstatadmin import DealStatAdmin
from analytics.site.incomestatadmin import IncomeStatAdmin
from analytics.site.leadsourcestatadmin import LeadSourceStatAdmin
from analytics.site.outputstatadmin import OutputStatAdmin
from analytics.site.requeststatadmin import RequestStatAdmin
from analytics.site.salesfunnelsadmin import SalesFunnelAdmin

from crm.site.crmadminsite import crm_site


@admin.register(IncomeStatSnapshot)
class IncomeStatSnapshotAdmin(ModelAdmin):
    """
    Admin for IncomeStatSnapshot using Unfold's ModelAdmin
    so it fully adopts Unfold styles & components.
    """

    list_display = (
        "creation_date",
        "id",
        "owner",
        "department",
        "modified_by",
    )
    list_display_links = ("id", "creation_date")
    list_filter = (
        "creation_date",
        "owner",
        "department",
    )
    search_fields = (
        "id",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
        "department__name",
    )
    date_hierarchy = "creation_date"
    ordering = ("-creation_date",)

    list_select_related = (
        "owner",
        "department",
        "modified_by",
    )

    list_per_page = 25


@admin.register(Permission)
class PermissionAdmin(ModelAdmin):
    """
    Use Unfold's ModelAdmin for Permission so it also matches
    the Unfold visual style and table layout.
    """

    list_display = (
        "name",
        "content_type",
        "codename",
    )
    list_filter = ("content_type",)
    search_fields = (
        "name",
        "codename",
        "content_type__app_label",
        "content_type__model",
    )
    ordering = ("content_type__app_label", "codename")
    list_per_page = 50


# CRM admin site registrations
crm_site.register(ClosingReasonStat, ClosingReasonStatAdmin)
crm_site.register(ConversionStat, ConversionStatAdmin)
crm_site.register(DealStat, DealStatAdmin)
crm_site.register(IncomeStat, IncomeStatAdmin)
crm_site.register(LeadSourceStat, LeadSourceStatAdmin)
crm_site.register(OutputStat, OutputStatAdmin)
crm_site.register(RequestStat, RequestStatAdmin)
crm_site.register(SalesFunnel, SalesFunnelAdmin)

# If you intentionally also want IncomeStat in the default admin site,
# keep this registration as well:
admin.site.register(IncomeStat, IncomeStatAdmin)
