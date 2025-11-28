from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin

from common.utils.for_translation import check_for_translation
from crm.site.crmadminsite import crm_site
from tasks.models import (
    Memo,
    Project,
    ProjectStage,
    Resolution,
    Tag,
    Task,
    TaskStage,
)
from tasks.site import memoadmin, projectadmin, taskadmin
from tasks.site.tagadmin import TagAdmin as BaseTagAdmin


class TranslateNameModelAdmin(ModelAdmin):
    """
    Base admin that triggers translation check on save.
    """

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        check_for_translation(request, obj, form)


@admin.register(Memo)
class MemoAdmin(memoadmin.MemoAdmin):
    """
    Memo admin in the default Django admin site, based on the project
    MemoAdmin but adapted for Unfold.
    """

    readonly_fields = [
        "name_icon",
        "creation_date",
        "modified_by",
        "status",
        "action",
        "date_of_review",
        "view_button",
        "update_date",
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            # Insert update_date + draft into the first fieldset
            fieldsets[0][1]["fields"].insert(
                2,
                ("update_date", "draft"),
            )
        return fieldsets


@admin.register(Project)
class ProjectAdmin(projectadmin.ProjectAdmin):
    """
    Project admin in the default site.
    """

    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (
                None,
                {
                    "fields": (
                        "name",
                        ("due_date", "priority"),
                        "description",
                        "note",
                        "stage",
                        "next_step",
                        "next_step_date",
                        "workflow_area",
                        ("creation_date", "closing_date"),
                        ("owner", "co_owner"),
                        "responsible_list",
                    )
                },
            ),
            (
                _("Change responsible"),
                {
                    "classes": ("collapse",),
                    "fields": ("responsible",),
                },
            ),
            (
                None,
                {
                    "fields": ("subscribers_list",),
                },
            ),
            (
                _("Change subscribers"),
                {
                    "classes": ("collapse",),
                    "fields": ("subscribers",),
                },
            ),
            (
                _("Additional information"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        "start_date",
                        "closing_date",
                        "active",
                    ),
                },
            ),
        ]
        fieldsets.extend(self.get_tag_fieldsets(obj))
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj=obj))
        # Owner should be editable here
        if "owner" in readonly_fields:
            readonly_fields.remove("owner")
        return readonly_fields


@admin.register(Resolution)
class ResolutionAdmin(TranslateNameModelAdmin):
    list_display = ("name", "index_number")
    ordering = ("index_number", "name")


@admin.register(Task)
class TaskAdmin(taskadmin.TaskAdmin):
    """
    Task admin in the default site.
    """

    # -- ModelAdmin methods -- #

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (
                None,
                {
                    "fields": (
                        "name",
                        ("due_date", "priority"),
                        "description",
                        "note",
                        ("stage", "hide_main_task"),
                        "next_step",
                        "next_step_date",
                        "workflow_area",
                        ("creation_date", "closing_date"),
                        ("owner", "co_owner"),
                        "responsible_list",
                    )
                },
            ),
            (
                _("Change responsible"),
                {
                    "classes": ("collapse",),
                    "fields": ("responsible",),
                },
            ),
            (
                None,
                {
                    "fields": ("subscribers_list",),
                },
            ),
            (
                _("Change subscribers"),
                {
                    "classes": ("collapse",),
                    "fields": ("subscribers",),
                },
            ),
            (
                _("Additional information"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        "task",
                        "project",
                        "hide_main_task",
                        "start_date",
                        "closing_date",
                        "active",
                        "token",
                    ),
                },
            ),
        ]
        fieldsets.extend(self.get_tag_fieldsets(obj))
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj=obj))
        # Owner should be editable; token should be read-only
        if "owner" in readonly_fields:
            readonly_fields.remove("owner")
        if "token" not in readonly_fields:
            readonly_fields.append("token")
        return readonly_fields


@admin.register(TaskStage)
class TaskStageAdmin(TranslateNameModelAdmin):
    list_display = (
        "name",
        "default",
        "active",
        "done",
        "in_progress",
        "index_number",
    )
    fields = (
        "name",
        "default",
        "active",
        "done",
        "in_progress",
        "index_number",
    )
    ordering = ("index_number", "name")


@admin.register(ProjectStage)
class ProjectStageAdmin(TranslateNameModelAdmin):
    list_display = (
        "name",
        "default",
        "active",
        "done",
        "in_progress",
        "index_number",
    )
    fields = (
        "name",
        "default",
        "active",
        "done",
        "in_progress",
        "index_number",
    )
    ordering = ("index_number", "name")


@admin.register(Tag)
class TagAdmin(BaseTagAdmin):
    """
    Use the project TagAdmin but register it here so Unfold styles apply
    in the default admin site.
    """
    pass


# --- CRM custom admin site registrations (unchanged) --- #

crm_site.register(Memo, memoadmin.MemoAdmin)
crm_site.register(Project, projectadmin.ProjectAdmin)
crm_site.register(Resolution, ResolutionAdmin)
crm_site.register(Tag, BaseTagAdmin)
crm_site.register(Task, taskadmin.TaskAdmin)
