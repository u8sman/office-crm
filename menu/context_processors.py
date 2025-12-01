from __future__ import annotations

from typing import Dict, Any

from django.conf import settings

from .models import MenuGroup


def unfold_dynamic_sidebar(request) -> Dict[str, Any]:
    """
    For every request:

    1. Read menu groups + items from DB.
    2. Build UNFOLD['SIDEBAR']['navigation'] structure.
    3. Write it back into settings.UNFOLD so Unfold uses it.

    We don't need to return UNFOLD in context; Unfold reads from settings.
    """

    # Make sure UNFOLD exists
    unfold = getattr(settings, "UNFOLD", {})
    if "SIDEBAR" not in unfold:
        unfold["SIDEBAR"] = {}

    sidebar = unfold["SIDEBAR"]

    navigation = []

    groups = MenuGroup.objects.prefetch_related("items").all()

    for group in groups:
        group_dict = {
            "title": group.title,
            "separator": group.separator,
            "collapsible": group.collapsible,
            "items": [],
        }

        for item in group.items.all():
            group_dict["items"].append(
                {
                    "title": item.title,
                    "icon": item.icon,
                    "link": item.link,
                }
            )

        # only show groups that have at least 1 item
        if group_dict["items"]:
            navigation.append(group_dict)

    sidebar["navigation"] = navigation
    unfold["SIDEBAR"] = sidebar
    settings.UNFOLD = unfold  # <-- update global settings used by Unfold

    # We don't need to expose anything special to templates here
    return {}
