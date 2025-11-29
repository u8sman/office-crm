from django.conf import settings
from django.shortcuts import redirect

class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Normalize prefixes
        self.admin_prefix = "/" + settings.SECRET_ADMIN_PREFIX.strip("/")
        self.crm_prefix = "/" + settings.SECRET_CRM_PREFIX.strip("/")

    def __call__(self, request):
        path = request.path

        # If admin prefix is empty, nothing to redirect
        if settings.SECRET_ADMIN_PREFIX == "":
            return self.get_response(request)

        # Only redirect if path begins with admin prefix
        if path.startswith(self.admin_prefix) and not request.user.is_superuser:
            # Remove prefix ONCE (not replace everywhere)
            trimmed = path[len(self.admin_prefix):]
            if not trimmed.startswith("/"):
                trimmed = "/" + trimmed

            # Build safe target path
            new_path = f"{self.crm_prefix}{trimmed}"

            # Add query string
            q = request.META.get("QUERY_STRING")
            if q:
                new_path = f"{new_path}?{q}"

            return redirect(new_path)

        return self.get_response(request)
