import threading

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin

from common.utils.helpers import LEADERS
from crm.site.crmadminsite import crm_site
from help.models import Page, Paragraph
from help.site import pageadmin

_thread_local = threading.local()


class HelpPageForm(forms.ModelForm):
    app_label = forms.ChoiceField(required=False)
    model = forms.ChoiceField(required=False)

    class Meta:
        model = Page
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["app_label"].choices = _thread_local.app_label_choices
        self.fields["model"].choices = _thread_local.model_choices
        self.initial["language_code"] = _thread_local.language_code


class ParagraphInline(admin.StackedInline):
    """
    Inline for Paragraphs on a Page. Works fine visually with Unfold.
    """

    model = Paragraph
    extra = 0
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "groups",
                    ("title", "language_code"),
                    "content",
                    "help_text",
                    ("draft", "verification_required"),
                    "index_number",
                    "link1",
                )
            },
        ),
    ]
    filter_horizontal = ("groups",)
    readonly_fields = ("language_code", "help_text")
    save_on_top = True

    class Media:
        js = (
            "/static/common/js/vendor/nicEdit.js",
            "/static/common/js/vendor/paragraph_textareas.js",
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if getattr(_thread_local, "obj", None):
            qs = qs.filter(
                language_code=_thread_local.obj.language_code,
                document=_thread_local.obj,
            )
        return qs.order_by("index_number")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            kwargs["queryset"] = Group.objects.exclude(department__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # -- StackedInline callables -- #

    @admin.display(description="")
    def help_text(self, obj):
        return _(
            "To add the correct link, use the tag /SECRET_CRM_PREFIX/ if necessary"
        )


@admin.register(Page)
class PageAdmin(ModelAdmin):
    """
    Unfold-styled admin for help Pages.
    """

    empty_value_display = LEADERS
    inlines = [ParagraphInline]

    list_display = (
        "title",
        "model",
        "page",
        "app_label",
        "language_code",
    )
    list_filter = (
        "language_code",
        "app_label",
        "model",
        "page",
    )
    search_fields = ["title", "paragraph__content"]
    save_on_top = True
    list_per_page = 25
    ordering = ("app_label", "model", "page", "language_code")

    def get_form(self, request, obj=None, **kwargs):
        """
        Build choices for app_label/model dynamically and inject into the custom form.
        """
        available_apps = self.admin_site.get_app_list(request)

        app_labels = [(x["app_label"], x["app_label"]) for x in available_apps]
        app_labels = [("", LEADERS)] + app_labels
        _thread_local.app_label_choices = app_labels

        if obj and obj.app_label:
            app = next(
                (x for x in available_apps if x["app_label"] == obj.app_label),
                None,
            )
            if app:
                model_choices = [
                    (m["object_name"], m["name"].capitalize())
                    for m in app["models"]
                ]
            else:
                model_choices = []
        else:
            model_choices = [
                (
                    m._meta.object_name,
                    m._meta.verbose_name_plural.capitalize(),
                )
                for m in self.admin_site._registry.keys()
            ]

        model_choices.sort(key=lambda x: x[1])
        model_choices = [("", LEADERS)] + model_choices
        _thread_local.model_choices = model_choices
        _thread_local.obj = obj

        if not obj:
            _thread_local.language_code = translation.get_language()
        else:
            _thread_local.language_code = obj.language_code

        # return custom form class for this admin
        return HelpPageForm

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.language_code:
                instance.language_code = _thread_local.language_code
            instance.save()
        formset.save_m2m()


@admin.register(Paragraph)
class ParagraphAdmin(ModelAdmin):
    """
    Unfold-styled admin for standalone Paragraph editing.
    """

    class Media:
        js = (
            "/static/common/js/vendor/nicEdit.js",
            "/static/common/js/vendor/paragraph_textareas.js",
        )

    list_display = (
        "title",
        "document",
        "language_code",
        "index_number",
        "draft",
        "verification_required",
    )
    list_filter = (
        "language_code",
        "document__page",
        "document__model",
        "draft",
        "verification_required",
    )
    raw_id_fields = ("document",)
    search_fields = ("content", "title")
    save_on_top = True
    ordering = ("document", "language_code", "index_number")
    list_per_page = 25


# Default Django admin site registrations
# (now using @admin.register above, so only Paragraph & Page for crm_site below)

crm_site.register(Page, pageadmin.PageAdmin)
