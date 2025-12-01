# menu/admin.py

from django import forms
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from unfold.admin import ModelAdmin, TabularInline

from .models import MenuGroup, MenuItem


def get_all_admin_urls():
    """
    Returns list of choices like:
    ("/admin/auth/user/", "auth / Users")
    ("/admin/auth/user/add/", "auth / Add User")
    """
    links = []

    for model, model_admin in admin.site._registry.items():
        opts = model._meta

        # Changelist
        list_name = f"admin:{opts.app_label}_{opts.model_name}_changelist"
        try:
            list_url = reverse(list_name)
            links.append((list_url, f"{opts.app_label} / {opts.verbose_name_plural.title()}"))
        except NoReverseMatch:
            pass

        # Add page
        add_name = f"admin:{opts.app_label}_{opts.model_name}_add"
        try:
            add_url = reverse(add_name)
            links.append((add_url, f"{opts.app_label} / Add {opts.verbose_name.title()}"))
        except NoReverseMatch:
            pass

    links.sort(key=lambda x: x[1])
    return links


class MenuItemInlineForm(forms.ModelForm):
    # Helper dropdown of admin URLs (optional)
    url_picker = forms.ChoiceField(
        label="Choose admin URL",
        required=False,
        choices=[],
        help_text="Pick an admin URL, then you can still tweak the link below.",
    )

    class Meta:
        model = MenuItem
        # include 'order' so Unfold can update it when sorting
        fields = ("icon", "title", "url_picker", "link", "order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ########### URL PICKER (DROPDOWN) ###########
        self.fields["url_picker"].choices = [("", "— Select admin URL —")] + get_all_admin_urls()

        # When user selects dropdown, auto-fill the link field
        self.fields["url_picker"].widget.attrs.update(
            {
                "onchange": (
                    "if(this.value){"
                    "const linkInput = document.getElementById(this.id.replace('url_picker','link'));"
                    "if(linkInput){ linkInput.value=this.value; linkInput.focus(); }"
                    "}"
                ),
                "style": (
                    "min-width: 260px; "
                    "padding: 6px 10px; "
                    "border-radius: 6px; "
                    "border: 1px solid #d1d5db; "
                    "background-color: #f9fafb; "
                    "font-size: 13px;"
                ),
            }
        )

        ########### ICON FIELD ###########
        # Simple label with info
        self.fields["icon"].label = 'Icon (see: fonts.google.com/icons)'

        # Styled icon input
        self.fields["icon"].widget.attrs.update(
            {
                "placeholder": "e.g. dashboard",
                "style": (
                    "min-width: 140px; "
                    "padding: 6px 8px; "
                    "border-radius: 6px; "
                    "border: 1px solid #d1d5db; "
                    "font-size: 13px;"
                ),
            }
        )
        self.fields["icon"].help_text = "Material icon name. Example: dashboard, people, settings."

        ########### TITLE FIELD ###########
        self.fields["title"].widget.attrs.update(
            {
                "placeholder": "Menu label (e.g. Users)",
                "style": (
                    "min-width: 200px; "
                    "padding: 6px 8px; "
                    "border-radius: 6px; "
                    "border: 1px solid #d1d5db; "
                    "font-size: 13px;"
                ),
            }
        )

        ########### LINK FIELD ###########
        self.fields["link"].widget.attrs.update(
            {
                "placeholder": "/admin/auth/user/  or  /crm/dashboard/",
                "style": (
                    "min-width: 300px; "
                    "padding: 6px 8px; "
                    "border-radius: 6px; "
                    "border: 1px solid #9ca3af; "
                    "font-size: 13px;"
                ),
            }
        )
        self.fields["link"].help_text = (
            "You can type any URL. Picking from the dropdown above will prefill this field."
        )


class MenuItemInlineFormSet(BaseInlineFormSet):
    """
    Custom validation:
    - If a row is completely empty → ignore it (no error)
    - If any field in the row is filled → icon, title, and link become required
    """

    def clean(self):
        super().clean()

        for form in self.forms:
            # Skip deleted rows
            if form.cleaned_data.get("DELETE"):
                continue

            # If form isn't valid at field level, skip extra logic (Django will show errors)
            if not hasattr(form, "cleaned_data"):
                continue

            icon = form.cleaned_data.get("icon")
            title = form.cleaned_data.get("title")
            link = form.cleaned_data.get("link")

            # "Empty row" = no values at all → ignore, no error
            if not (icon or title or link):
                continue

            # Row has something → enforce required fields
            if not icon:
                form.add_error("icon", "This field is required.")
            if not title:
                form.add_error("title", "This field is required.")
            if not link:
                form.add_error("link", "This field is required.")


class MenuItemInline(TabularInline):
    """
    Inline menu items displayed under MenuGroup form.

    Columns:
    [drag handle] [icon] [title] [URL picker] [link] [delete]
    """

    model = MenuItem
    form = MenuItemInlineForm
    formset = MenuItemInlineFormSet

    extra = 0  # no empty rows unless needed; you can set 1 if you prefer

    # Unfold sortable inline (uses MenuItem.order)
    ordering_field = "order"
    hide_ordering_field = True  # Unfold hides the column, but it's still in the form

    # include 'order' so Unfold JS can update it on drag
    fields = ("icon", "title", "url_picker", "link", "order")
    list_display = ["icon", "title", "link", "order"]


@admin.register(MenuGroup)
class MenuGroupAdmin(ModelAdmin):
    """
    “Manage menu” screen:

    - Unfold-styled list of groups
    - Drag & drop groups via `order`
    - Inline menu organizer under each group
    """

    ordering_field = "order"
    hide_ordering_field = True

    list_display = ("title", "collapsible", "separator", "order")
    exclude = ("order",)

    inlines = [MenuItemInline]
