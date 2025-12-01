# menu/models.py

from django.db import models
from django.db.models import Max


class MenuGroup(models.Model):
    title = models.CharField(max_length=100)

    separator = models.BooleanField(
        default=False,
        help_text="Show a separator line before this group.",
    )

    collapsible = models.BooleanField(
        default=True,
        help_text="Allow this group to be collapsed in the sidebar.",
    )

    # Unfold sortable changelist: PositiveIntegerField + db_index=True
    order = models.PositiveIntegerField(
        "order",
        default=0,
        db_index=True,
        help_text="Sorting order in sidebar (auto-assigned).",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Menu group"
        verbose_name_plural = "Menu groups"  # name in admin sidebar

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # If new and order not set, put at end
        if self.pk is None and (self.order is None or self.order == 0):
            max_order = MenuGroup.objects.aggregate(max_o=Max("order"))["max_o"] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class MenuItem(models.Model):
    group = models.ForeignKey(
        MenuGroup,
        related_name="items",
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=100)

    icon = models.CharField(
        max_length=50,
        help_text="Material icon name (e.g. 'dashboard', 'people').",
    )

    link = models.CharField(
        max_length=255,
        help_text="Final URL, e.g. '/admin/auth/user/'.",
    )

    # Unfold sortable inline: PositiveIntegerField + db_index=True
    order = models.PositiveIntegerField(
        "order",
        default=0,
        db_index=True,
        help_text="Order inside this group (auto-assigned).",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # If new and no order, put at end of this group
        if self.pk is None and (self.order is None or self.order == 0) and self.group_id:
            max_order = (
                MenuItem.objects.filter(group=self.group)
                .aggregate(max_o=Max("order"))["max_o"]
                or 0
            )
            self.order = max_order + 1
        super().save(*args, **kwargs)
