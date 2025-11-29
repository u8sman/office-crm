import sys
from pathlib import Path
from datetime import datetime as dt
from django.utils.translation import gettext_lazy as _
import environ
import os

from crm.settings import *          # NOQA
from common.settings import *       # NOQA
from tasks.settings import *        # NOQA
from voip.settings import *         # NOQA
from .datetime_settings import *    # NOQA

# ---- Django settings ---- #

BASE_DIR = Path(__file__).resolve().parent.parent

# Env
env = environ.Env(
    DEBUG=(bool, False),
)

# Read .env only locally; Render will inject real env vars
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# SECURITY WARNING: don’t hardcode this in production!
SECRET_KEY = env(
    "SECRET_KEY",
    default="dev-only-secret-key-change-me"
)

# Debug controlled via env
DEBUG = env.bool("DEBUG", default=False)

# Hosts
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["127.0.0.1", "office-crm.onrender.com", "crm.power-devs.com"]
)

CSRF_TRUSTED_ORIGINS = [
    "https://office-crm.onrender.com",
    "https://crm.power-devs.com",
]

# Database – using discrete env vars (Aiven)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="defaultdb"),
        "USER": env("DB_USER", default="avnadmin"),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# Email (move secrets to env)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="crm@example.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default="CRM: ")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=10)

SERVER_EMAIL = env("SERVER_EMAIL", default="test@example.com")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="test@example.com")

ADMINS = [
    (env("ADMIN_NAME", default="Admin"), env("ADMIN_EMAIL", default="u8sman@gmail.com"))
]

# Internationalization
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("ar", "Arabic"),
    ("cs", "Czech"),
    ("de", "German"),
    ("el", "Greek"),
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("he", "Hebrew"),
    ("hi", "Hindi"),
    ("id", "Indonesian"),
    ("it", "Italian"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
    ("nl", "Nederlands"),
    ("pl", "Polish"),
    ("pt-br", "Portuguese"),
    ("ro", "Romanian"),
    ("ru", "Russian"),
    ("tr", "Turkish"),
    ("uk", "Ukrainian"),
    ("vi", "Vietnamese"),
    ("zh-hans", "Chinese"),
]

TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

LOGIN_URL = "/admin/login/"

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    "unfold.contrib.constance",

    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "crm.apps.CrmConfig",
    "massmail.apps.MassmailConfig",
    "analytics.apps.AnalyticsConfig",
    "help",
    "tasks.apps.TasksConfig",
    "chat.apps.ChatConfig",
    "voip",
    "common.apps.CommonConfig",
    "settings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",    # for static on Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "common.utils.admin_redirect_middleware.AdminRedirectMiddleware",
    "common.utils.usermiddleware.UserMiddleware",
]


ROOT_URLCONF = "webcrm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webcrm.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Static / Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise – efficient static serving on Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Local-only extra static folders
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "static_custom",
    ]

FIXTURE_DIRS = ["tests/fixtures"]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

SITE_ID = 1

# Security – stricter in production
# if not DEBUG:
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
# else:
#     SECURE_HSTS_SECONDS = 0
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = False
#     SECURE_HSTS_PRELOAD = False
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False

X_FRAME_OPTIONS = "SAMEORIGIN"


# ---- CRM settings ---- #

# For more security, replace the url prefixes
# with your own unique value.
SECRET_CRM_PREFIX = "crm-user/"
SECRET_ADMIN_PREFIX = "admin/"
SECRET_LOGIN_PREFIX = "login/"

# Specify ip of host to avoid importing emails sent by CRM
CRM_IP = "74.220.48.0/24"

CRM_REPLY_TO = ["'Do not reply' <u8sman@gmail.com>"]

# List of addresses to which users are not allowed to send mail.
NOT_ALLOWED_EMAILS = []

# List of applications on the main page and in the left sidebar.
APP_ON_INDEX_PAGE = [
    "tasks",
    "crm",
    "analytics",
    "massmail",
    "common",
    "settings",
]
MODEL_ON_INDEX_PAGE = {
    "tasks": {
        "app_model_list": ["Task", "Memo"]
    },
    "crm": {
        "app_model_list": [
            "Request",
            "Deal",
            "Lead",
            "Company",
            "CrmEmail",
            "Payment",
            "Shipment",
        ]
    },
    "analytics": {
        "app_model_list": [
            "IncomeStat",
            "RequestStat",
        ]
    },
    "massmail": {
        "app_model_list": [
            "MailingOut",
            "EmlMessage",
        ]
    },
    "common": {
        "app_model_list": [
            "UserProfile",
            "Reminder",
        ]
    },
    "settings": {
        "app_model_list": [
            "PublicEmailDomain",
            "StopPhrase",
        ]
    },
}

# Country VAT value
VAT = 0    # %

# 2-Step Verification Credentials for Google Accounts.
#  OAuth 2.0
CLIENT_ID = ""
CLIENT_SECRET = ""
OAUTH2_DATA = {
    "smtp.gmail.com": {
        "scope": "https://mail.google.com/",
        "accounts_base_url": "https://accounts.google.com",
        "auth_command": "o/oauth2/auth",
        "token_command": "o/oauth2/token",
    }
}
# Hardcoded dummy redirect URI for non-web apps.
REDIRECT_URI = ""

# Credentials for Google reCAPTCHA.
GOOGLE_RECAPTCHA_SITE_KEY = ""
GOOGLE_RECAPTCHA_SECRET_KEY = ""

GEOIP = False
GEOIP_PATH = MEDIA_ROOT / "geodb"

# For user profile list
SHOW_USER_CURRENT_TIME_ZONE = False

NO_NAME_STR = _("Untitled")

# For automated getting currency exchange rate
LOAD_EXCHANGE_RATE = False
LOADING_EXCHANGE_RATE_TIME = "6:30"
LOAD_RATE_BACKEND = ""  # "crm.backends.<specify_backend>.<specify_class>"

# Ability to mark payments through a representation
MARK_PAYMENTS_THROUGH_REP = False

# Site headers
SITE_TITLE = "CRM"
ADMIN_HEADER = "ADMIN"
ADMIN_TITLE = "CRM Admin"
INDEX_TITLE = _("Main Menu")

# Allow mailing
MAILING = True

# This is copyright information. Please don't change it!
COPYRIGHT_STRING = f"Django-CRM. Copyright (c) {dt.now().year}"
PROJECT_NAME = "Django-CRM"
PROJECT_SITE = "https://djangocrm.github.io/info/"

TESTING = sys.argv[1:2] == ["test"]
if TESTING:
    SECURE_SSL_REDIRECT = False
    LANGUAGE_CODE = "en"
    LANGUAGES = [("en", ""), ("uk", "")]


# settings.py
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def permission_superuser(request):
    return request.user.is_superuser


def tabs_permission(request):
    # keep simple for now
    return True


UNFOLD = {
    "SITE_TITLE": "Office CRM",
    "SITE_HEADER": "Office CRM",
    "SITE_SUBHEADER": "Sales & Client Management",
    "SITE_URL": "/",

    "SITE_SYMBOL": "speed",

    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,

    # optional theme
    "THEME": None,  # or "light" / "dark"
    "BORDER_RADIUS": "8px",

    "STYLES": [
        lambda request: static("css/custom-forms.css"),
        lambda request: static("css/custom.css"),
    ],

    # "STYLES": [
    #     lambda request: static("css/admin-extra.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/admin-extra.js"),
    # ],

    "SITE_DROPDOWN": [
        {
            "icon": "task_alt",
            "title": _("Basecamp Tasks"),
            "link": "https://office.power-devs.com/",
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "bug_report",  # material icon name
            "title": _("Report Bug"),
            "link": "https://docs.google.com/spreadsheets/d/1i-PzJvntcrRcWIXhLE5Hzgvxc8FRC62oRhdcR5HygB4/edit?gid=292726321#gid=292726321",
            # On newer Unfold versions you can also do:
            # "attrs": {"target": "_blank"},
        },
    ],

    # SIDEBAR – keep this shape
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": True,   # hide auto-generated Django sidebar
        "navigation": [

            {
                "title": _("Shortcuts"),
                "items": [
                    {
                        "title": _("Basecamp Tasks"),
                        "icon": "task_alt",
                        "link": "https://office.power-devs.com/",
                        "new_window": True,
                    },
                    {
                        "title": _("Report Bug"),
                        "icon": "bug_report",
                        "link": "https://docs.google.com/spreadsheets/d/1i-PzJvntcrRcWIXhLE5Hzgvxc8FRC62oRhdcR5HygB4/edit?gid=292726321#gid=292726321",
                        "new_window": True,
                    },
                ],
            },


            # # -----------------------------
            # # Administration
            # # -----------------------------
            # {
            #     "title": "Administration",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {
            #             "title": "Log entries",
            #             "icon": "receipt_long",
            #             "link": "/en/admin/logentry/",
            #             "actions": [
            #                 {
            #                     "title": "Add",
            #                     "icon": "add",
            #                     "link": "/en/admin/logentry/add/",
            #                 }
            #             ],
            #         },
            #     ],
            # },
            #
            # # -----------------------------
            # # Analytics
            # # -----------------------------
            # {
            #     "title": "Analytics",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {
            #             "title": "Income Summary",
            #             "icon": "insights",
            #             "link": "/en/analytics/incomestat/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/analytics/incomestat/add/"}
            #             ],
            #         },
            #         {
            #             "title": "IncomeStat Snapshots",
            #             "icon": "monitoring",
            #             "link": "/en/analytics/incomestatsnapshot/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/analytics/incomestatsnapshot/add/"}
            #             ],
            #         },
            #     ],
            # },
            #
            # # -----------------------------
            # # Authentication
            # # -----------------------------
            # {
            #     "title": "Authentication & Authorization",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {
            #             "title": "Groups",
            #             "icon": "group",
            #             "link": "/en/auth/group/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/auth/group/add/"}
            #             ],
            #         },
            #         {
            #             "title": "Permissions",
            #             "icon": "lock",
            #             "link": "/en/auth/permission/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/auth/permission/add/"}
            #             ],
            #         },
            #         {
            #             "title": "Users",
            #             "icon": "person",
            #             "link": "/en/auth/user/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/auth/user/add/"}
            #             ],
            #         },
            #     ],
            # },
            #
            # # -----------------------------
            # # Chat
            # # -----------------------------
            # {
            #     "title": "Chat",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {
            #             "title": "Messages",
            #             "icon": "chat",
            #             "link": "/en/chat/chatmessage/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/chat/chatmessage/add/"}
            #             ],
            #         },
            #     ],
            # },
            #
            # # -----------------------------
            # # Common
            # # -----------------------------
            # {
            #     "title": "Common",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title": "Departments", "icon": "work", "link": "/en/common/department/", "actions":[{"title":"Add","icon":"add","link":"/en/common/department/add/"}]},
            #         {"title": "Files", "icon": "folder", "link": "/en/common/thefile/", "actions":[{"title":"Add","icon":"add","link":"/en/common/thefile/add/"}]},
            #         {"title": "Reminders", "icon": "alarm", "link": "/en/common/reminder/", "actions":[{"title":"Add","icon":"add","link":"/en/common/reminder/add/"}]},
            #         {"title": "User profiles", "icon": "badge", "link": "/en/common/userprofile/", "actions":[{"title":"Add","icon":"add","link":"/en/common/userprofile/add/"}]},
            #     ],
            # },
            #
            # # -----------------------------
            # # CRM
            # # -----------------------------
            # {
            #     "title": "CRM",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title":"Cities","icon":"location_city","link":"/en/crm/city/","actions":[{"title":"Add","icon":"add","link":"/en/crm/city/add/"}]},
            #         {"title":"Closing reasons","icon":"cancel","link":"/en/crm/closingreason/","actions":[{"title":"Add","icon":"add","link":"/en/crm/closingreason/add/"}]},
            #         {"title":"Companies","icon":"business","link":"/en/crm/company/","actions":[{"title":"Add","icon":"add","link":"/en/crm/company/add/"}]},
            #         {"title":"Contact persons","icon":"contacts","link":"/en/crm/contact/","actions":[{"title":"Add","icon":"add","link":"/en/crm/contact/add/"}]},
            #         {"title":"Countries","icon":"public","link":"/en/crm/country/","actions":[{"title":"Add","icon":"add","link":"/en/crm/country/add/"}]},
            #         {"title":"Currencies","icon":"payments","link":"/en/crm/currency/","actions":[{"title":"Add","icon":"add","link":"/en/crm/currency/add/"}]},
            #         {"title":"Currency rates","icon":"trending_up","link":"/en/crm/rate/","actions":[{"title":"Add","icon":"add","link":"/en/crm/rate/add/"}]},
            #         {"title":"Deals","icon":"handshake","link":"/en/crm/deal/","actions":[{"title":"Add","icon":"add","link":"/en/crm/deal/add/"}]},
            #         {"title":"Emails in CRM","icon":"mail","link":"/en/crm/crmemail/","actions":[{"title":"Add","icon":"add","link":"/en/crm/crmemail/add/"}]},
            #         {"title":"Industries of Clients","icon":"factory","link":"/en/crm/industry/","actions":[{"title":"Add","icon":"add","link":"/en/crm/industry/add/"}]},
            #         {"title":"Lead Sources","icon":"source","link":"/en/crm/leadsource/","actions":[{"title":"Add","icon":"add","link":"/en/crm/leadsource/add/"}]},
            #         {"title":"Leads","icon":"assignment","link":"/en/crm/lead/","actions":[{"title":"Add","icon":"add","link":"/en/crm/lead/add/"}]},
            #         {"title":"Payments","icon":"attach_money","link":"/en/crm/payment/","actions":[{"title":"Add","icon":"add","link":"/en/crm/payment/add/"}]},
            #         {"title":"Product categories","icon":"category","link":"/en/crm/productcategory/","actions":[{"title":"Add","icon":"add","link":"/en/crm/productcategory/add/"}]},
            #         {"title":"Products","icon":"inventory","link":"/en/crm/product/","actions":[{"title":"Add","icon":"add","link":"/en/crm/product/add/"}]},
            #         {"title":"Requests","icon":"help","link":"/en/crm/request/","actions":[{"title":"Add","icon":"add","link":"/en/crm/request/add/"}]},
            #         {"title":"Shipments","icon":"local_shipping","link":"/en/crm/shipment/","actions":[{"title":"Add","icon":"add","link":"/en/crm/shipment/add/"}]},
            #         {"title":"Stages","icon":"timeline","link":"/en/crm/stage/","actions":[{"title":"Add","icon":"add","link":"/en/crm/stage/add/"}]},
            #         {"title":"Tags","icon":"sell","link":"/en/crm/tag/","actions":[{"title":"Add","icon":"add","link":"/en/crm/tag/add/"}]},
            #         {"title":"Types of Clients","icon":"groups","link":"/en/crm/clienttype/","actions":[{"title":"Add","icon":"add","link":"/en/crm/clienttype/add/"}]},
            #     ],
            # },
            #
            # # -----------------------------
            # # Help
            # # -----------------------------
            # {
            #     "title": "Help",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title":"Help pages","icon":"help_center","link":"/en/help/page/","actions":[{"title":"Add","icon":"add","link":"/en/help/page/add/"}]},
            #         {"title":"Paragraphs","icon":"description","link":"/en/help/paragraph/","actions":[{"title":"Add","icon":"add","link":"/en/help/paragraph/add/"}]},
            #     ],
            # },

            # -----------------------------
            # Mass mail
            # -----------------------------
            {
                "title": "Mass mail",
                "separator": True,
                "collapsible": False,
                "collapsed": False,
                "items": [
                    {"title":"Email Accounts","icon":"alternate_email","link":"/en/massmail/emailaccount/","actions":[{"title":"Add","icon":"add","link":"/en/massmail/emailaccount/add/"}]},
                    {"title":"Email Messages","icon":"mail","link":"/en/massmail/emlmessage/","actions":[{"title":"Add","icon":"add","link":"/en/massmail/emlmessage/add/"}]},
                    {"title":"Eml accounts queues","icon":"queue","link":"/en/massmail/emlaccountsqueue/","actions":[{"title":"Add","icon":"add","link":"/en/massmail/emlaccountsqueue/add/"}]},
                    {"title":"Mailing Outs","icon":"outbox","link":"/en/massmail/mailingout/","actions":[{"title":"Add","icon":"add","link":"/en/massmail/mailingout/add/"}]},
                    {"title":"Mass contacts","icon":"people","link":"/en/massmail/masscontact/","actions":[{"title":"Add","icon":"add","link":"/en/massmail/masscontact/add/"}]},
                    {"title":"Signatures","icon":"draw","link":"/en/massmail/signature/","actions":[{"title":"Add","icon":"add","link":"/en/massmail/signature/add/"}]},
                ],
            },

            # # -----------------------------
            # # Settings
            # # -----------------------------
            # {
            #     "title": "Settings",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title":"Banned company names","icon":"block","link":"/en/settings/bannedcompanyname/","actions":[{"title":"Add","icon":"add","link":"/en/settings/bannedcompanyname/add/"}]},
            #         {"title":"Massmail Settings","icon":"settings","link":"/en/settings/massmailsettings/","actions":[{"title":"Add","icon":"add","link":"/en/settings/massmailsettings/add/"}]},
            #         {"title":"Public email domains","icon":"public","link":"/en/settings/publicemaildomain/","actions":[{"title":"Add","icon":"add","link":"/en/settings/publicemaildomain/add/"}]},
            #         {"title":"Reminder settings","icon":"alarm_on","link":"/en/settings/reminders/","actions":[{"title":"Add","icon":"add","link":"/en/settings/reminders/add/"}]},
            #         {"title":"Stop Phrases","icon":"stop","link":"/en/settings/stopphrase/","actions":[{"title":"Add","icon":"add","link":"/en/settings/stopphrase/add/"}]},
            #     ],
            # },
            #
            # # -----------------------------
            # # Sites
            # # -----------------------------
            # {
            #     "title": "Sites",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title":"Sites","icon":"language","link":"/en/sites/site/","actions":[{"title":"Add","icon":"add","link":"/en/sites/site/add/"}]},
            #     ],
            # },
            #
            # # -----------------------------
            # # Tasks
            # # -----------------------------
            # {
            #     "title": "Tasks",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title":"Memos","icon":"sticky_note_2","link":"/en/tasks/memo/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/memo/add/"}]},
            #         {"title":"Project stages","icon":"layers","link":"/en/tasks/projectstage/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/projectstage/add/"}]},
            #         {"title":"Projects","icon":"folder_open","link":"/en/tasks/project/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/project/add/"}]},
            #         {"title":"Resolutions","icon":"check_circle","link":"/en/tasks/resolution/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/resolution/add/"}]},
            #         {"title":"Tags","icon":"sell","link":"/en/tasks/tag/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/tag/add/"}]},
            #         {"title":"Task stages","icon":"timeline","link":"/en/tasks/taskstage/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/taskstage/add/"}]},
            #         {"title":"Tasks","icon":"task","link":"/en/tasks/task/","actions":[{"title":"Add","icon":"add","link":"/en/tasks/task/add/"}]},
            #     ],
            # },
            #
            # # -----------------------------
            # # VoIP
            # # -----------------------------
            # {
            #     "title": "VoIP",
            #     "separator": True,
            #     "collapsible": True,
            #     "collapsed": True,
            #     "items": [
            #         {"title":"Connections","icon":"call","link":"/en/voip/connection/","actions":[{"title":"Add","icon":"add","link":"/en/voip/connection/add/"}]},
            #     ],
            # },

        ],
    },

    # # TABS – keep it simple and matching docs
    # "TABS": [
    #     {
    #         "models": [
    #             "tasks.task",   # app_label.model_name_in_lowercase
    #         ],
    #         "items": [
    #             {
    #                 "title": _("All"),
    #                 "link": reverse_lazy("admin:tasks_task_changelist"),
    #                 "permission": "webcrm.settings.tabs_permission",
    #             },
    #             # For filtered tabs, use plain strings (no reverse_lazy + concat)
    #             {
    #                 "title": _("Open"),
    #                 "link": "/en/tasks/task/?status__exact=open",
    #                 "permission": "webcrm.settings.tabs_permission",
    #             },
    #             {
    #                 "title": _("Completed"),
    #                 "link": "/en/tasks/task/?status__exact=done",
    #                 "permission": "webcrm.settings.tabs_permission",
    #             },
    #         ],
    #     },
    # ],
}


