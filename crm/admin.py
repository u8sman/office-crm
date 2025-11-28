from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.auth.models import Group
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin

from common.models import Department
from common.utils.for_translation import check_for_translation
from common.utils.helpers import LEADERS
from crm.models import (
    City,
    ClientType,
    ClosingReason,
    Company,
    Contact,
    Country,
    CrmEmail,
    Currency,
    Deal,
    Industry,
    Lead,
    LeadSource,
    Payment,
    Rate,
    Request,
    Shipment,
    Stage,
    Tag,
)
from crm.models.product import Product, ProductCategory
from crm.site import (
    cityadmin,
    companyadmin,
    contactadmin,
    crmemailadmin,
    dealadmin,
    leadadmin,
    productadmin,
    requestadmin,
    tagadmin,
)
from crm.site.currencyadmin import CurrencyAdmin
from crm.site.paymentadmin import PaymentAdmin
from crm.site.shipmentadmin import ShipmentAdmin
from crm.site.crmadminsite import crm_site
from crm.utils.admfilters import ByDepartmentFilter

admin.site.empty_value_display = "(None)"


class MyModelAdmin(ModelAdmin):
    """
    Base admin for CRM models that should always be filtered by department.
    Uses Unfold's ModelAdmin as the visual base.
    """

    list_filter = (ByDepartmentFilter,)

    # -- ModelAdmin methods -- #

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            kwargs["queryset"] = Group.objects.filter(department__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TranslateNameModelAdmin(MyModelAdmin):
    """
    Base admin with index shifting + translation check on save.
    """

    # -- ModelAdmin methods -- #

    def save_model(self, request, obj, form, change):
        if "index_number" in form.changed_data:
            # arrange indexes
            objects = self.model.objects.filter(
                index_number__gte=obj.index_number,
                department=obj.department,
            )
            objects.update(index_number=F("index_number") + 1)

        super().save_model(request, obj, form, change)
        check_for_translation(request, obj, form)


@admin.register(Company)
class CompanyAdmin(companyadmin.CompanyAdmin):
    """
    Company admin for the default Django admin site,
    customized but still based on the original companyadmin.CompanyAdmin.
    """

    inlines = []
    raw_id_fields = ("city",)

    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        return (
            (
                None,
                {
                    "fields": (
                        ("full_name", "disqualified"),
                        ("alternative_names", "massmail"),
                        ("type", "lead_source"),
                        "registration_number",
                        "was_in_touch",
                        "description",
                        "industry",
                    )
                },
            ),
            (None, {"fields": ("tag_list",)}),
            (
                _("Add tags"),
                {
                    "classes": ("collapse",),
                    "fields": ("tags",),
                },
            ),
            (
                _("Contact details"),
                {
                    "fields": (
                        ("email", "phone"),
                        "website",
                        "city_name",
                        ("city", "country"),
                        "region",
                        "district",
                        "address",
                    )
                },
            ),
            (
                _("Additional information"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        ("owner", "modified_by"),
                        "department",
                        "warning",
                        ("creation_date", "update_date"),
                    ),
                },
            ),
        )

    # -- ModelAdmin callables -- #

    @admin.display(description=_("Name"), ordering="name")
    def city_name(self, instance):
        if not instance.name:
            instance.name = settings.NO_NAME_STR
        return instance.name


@admin.register(Deal)
class DealAdmin(dealadmin.DealAdmin):
    list_display = [
        "dynamic_name",
        "next_step_name",
        "next_step_date",
        "stage",
        "owner",
        "relevant",
        "active",
        "counterparty",
        "creation_date",
    ]
    raw_id_fields = (
        "lead",
        "contact",
        "company",
        "partner_contact",
        "request",
    )

    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        return (
            (
                None,
                {
                    "fields": (
                        "name",
                        ("creation_date", "closing_date"),
                        ("inquiry", "translation"),
                        (
                            "relevant",
                            "active",
                            "important",
                            "closing_reason",
                        ),
                    )
                },
            ),
            (
                _("Contact info"),
                {
                    "fields": (
                        "contact_person",
                        "company",
                    )
                },
            ),
            (
                " ",
                {
                    "fields": (
                        "stage",
                        ("amount", "currency"),
                        "next_step",
                        "next_step_date",
                        "workflow",
                        "description",
                        "stages_dates",
                    )
                },
            ),
            (None, {"fields": ("tag_list",)}),
            (
                _("Add tags"),
                {
                    "classes": ("collapse",),
                    "fields": ("tags",),
                },
            ),
            (
                _("Relations"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        "contact",
                        "company",
                        "lead",
                        "partner_contact",
                        "request",
                    ),
                },
            ),
            (
                _("Additional information"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        ("owner", "co_owner"),
                        "department",
                        "update_date",
                        "modified_by",
                        "ticket",
                    ),
                },
            ),
        )

    def get_readonly_fields(self, request, obj=None):
        return (
            "inquiry",
            "company",
            "tag_list",
            "deal_messengers",
            "translation",
            "contact_person",
            "update_date",
            "creation_date",
            "dynamic_name",
            "counterparty",
        )


@admin.register(Contact)
class ContactAdmin(contactadmin.ContactAdmin):
    readonly_fields = ["creation_date", "update_date"]

    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        return (
            [
                None,
                {
                    "fields": (
                        ("first_name", "middle_name", "last_name"),
                        ("title", "sex"),
                        ("birth_date", "was_in_touch"),
                        ("disqualified", "massmail"),
                    )
                },
            ],
            (
                _("Add tags"),
                {
                    "fields": ("tags",),
                },
            ),
            (
                _("Contact details"),
                {
                    "fields": (
                        ("email", "secondary_email"),
                        "phone",
                        ("other_phone", "mobile"),
                        ("lead_source", "company"),
                        "region",
                        "district",
                        "address",
                        "country",
                    )
                },
            ),
            (
                _("Additional information"),
                {
                    "fields": (
                        ("owner", "department"),
                        "modified_by",
                        ("creation_date", "update_date"),
                    )
                },
            ),
        )


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Lead)
class LeadAdmin(leadadmin.LeadAdmin):
    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        return (
            (
                None,
                {
                    "fields": [
                        ("lead_source", "disqualified", "massmail"),
                        ("contact", "company"),
                    ],
                },
            ),
            (
                None,
                {
                    "fields": [
                        ("first_name", "middle_name", "last_name"),
                        ("title", "sex"),
                        ("birth_date", "was_in_touch"),
                        "description",
                    ],
                },
            ),
            (None, {"fields": ("tag_list",)}),
            (
                _("Add tags"),
                {
                    "classes": ("collapse",),
                    "fields": ("tags",),
                },
            ),
            (
                _("Contact details"),
                {
                    "fields": (
                        ("email", "secondary_email"),
                        ("phone", "other_phone"),
                        ("company_name", "website"),
                        ("company_email", "country"),
                        "region",
                        "district",
                        "address",
                    )
                },
            ),
            (
                _("Additional information"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        ("owner", "modified_by"),
                        "department",
                        ("creation_date", "update_date"),
                    ),
                },
            ),
        )


@admin.register(CrmEmail)
class CrmEmailAdmin(ModelAdmin):
    empty_value_display = LEADERS
    raw_id_fields = (
        "deal",
        "contact",
        "company",
        "request",
        "lead",
    )
    save_on_top = True


@admin.register(Request)
class RequestAdmin(requestadmin.RequestAdmin):
    raw_id_fields = (
        "lead",
        "contact",
        "deal",
        "company",
    )
    readonly_fields = tuple()

    def get_fieldsets(self, request, obj=None):
        return (
            (
                None,
                {
                    "fields": [
                        "request_for",
                        "duplicate",
                        "case",
                        "pending",
                        "subsequent",
                        ("lead_source", "receipt_date"),
                        ("department", "owner", "co_owner"),
                        ("first_name", "middle_name", "last_name"),
                        ("email", "phone"),
                        "website",
                        "company_name",
                        ("country", "city_name"),
                        ("description", "translation"),
                        "remark",
                        "products",
                    ]
                },
            ),
            (
                _("Relations"),
                {
                    "fields": [
                        "verification_required",
                        "contact",
                        "company",
                        "lead",
                        "deal",
                    ]
                },
            ),
            (
                _("Additional information"),
                {
                    "classes": ("collapse",),
                    "fields": [
                        "subsequent",
                        ("modified_by", "ticket"),
                    ],
                },
            ),
        )


@admin.register(Stage)
class StageAdmin(TranslateNameModelAdmin):
    list_display = (
        "name",
        "default",
        "second_default",
        "success_stage",
        "conditional_success_stage",
        "goods_shipped",
        "department",
        "index_number",
        "id",
    )
    list_filter = (
        ByDepartmentFilter,
        "default",
        "success_stage",
        "conditional_success_stage",
        "goods_shipped",
    )
    readonly_fields = ("id",)
    ordering = ("department", "index_number")


@admin.register(ClientType)
class ClientTypeAdmin(TranslateNameModelAdmin):
    list_display = ("name", "id", "department")
    ordering = ("department", "name")


@admin.register(Industry)
class IndustryAdmin(TranslateNameModelAdmin):
    list_display = ("name", "id", "department")
    ordering = ("department", "name")


@admin.register(Product)
class ProductAdmin(productadmin.ProductAdmin):
    list_display = ("name", "price", "currency", "department")

    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(self.fieldsets)
        fls = fieldsets[1][1]["fields"]
        if "department" not in fls:
            fls.extend(["department"])
        return fieldsets


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslateNameModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "name",
                    "department",
                    "description",
                    "creation_date",
                ]
            },
        ),
    )
    list_display = ("name", "id", "department")
    readonly_fields = ("creation_date",)


@admin.register(ClosingReason)
class ClosingReasonAdmin(TranslateNameModelAdmin):
    list_display = (
        "name",
        "id",
        "department",
        "index_number",
        "success_reason",
    )


@admin.register(LeadSource)
class LeadSourceAdmin(TranslateNameModelAdmin):
    list_display = (
        "name",
        "website_email",
        "department",
        "id",
    )
    raw_id_fields = ("department",)
    readonly_fields = ("website_email",)
    search_fields = ("name", "email", "uuid")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            kwargs["queryset"] = Department.objects.all()
        return BaseModelAdmin.formfield_for_foreignkey(
            self, db_field, request, **kwargs
        )

    # -- ModelAdmin Callables -- #

    @admin.display(
        description="Email on website",
        ordering="email",
    )
    def website_email(self, obj):
        return obj.email


@admin.register(Rate)
class RateAdmin(ModelAdmin):
    list_display = (
        "currency",
        "payment_date",
        "rate_to_state_currency",
        "rate_to_marketing_currency",
        "rate_type",
    )
    readonly_fields = ("payment_date",)
    ordering = ("-payment_date",)
    list_select_related = ("currency",)


# --- Registrations that use pre-defined admin classes from other modules --- #

admin.site.register(City, cityadmin.CityAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Tag, tagadmin.TagAdmin)

# --- CRM custom admin site registrations (unchanged) --- #

crm_site.register(City, cityadmin.CityAdmin)
crm_site.register(Company, companyadmin.CompanyAdmin)
crm_site.register(Contact, contactadmin.ContactAdmin)
crm_site.register(CrmEmail, crmemailadmin.CrmEmailAdmin)
crm_site.register(Currency, CurrencyAdmin)
crm_site.register(Deal, dealadmin.DealAdmin)
crm_site.register(Lead, leadadmin.LeadAdmin)
crm_site.register(Payment, PaymentAdmin)
crm_site.register(Product, productadmin.ProductAdmin)
crm_site.register(Request, requestadmin.RequestAdmin)
crm_site.register(Shipment, ShipmentAdmin)
crm_site.register(Tag, tagadmin.TagAdmin)
