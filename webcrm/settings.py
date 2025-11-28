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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent



# Initialize environment reader
env = environ.Env()

# Path to .env file
env_file = os.path.join(BASE_DIR, ".env")

if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# SECURITY WARNING: keep the secret key used in production secret!
# To get new value of key use code:
# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())
SECRET_KEY = 'j1c=6$s-dh#$ywt@(q4cm=j&0c*!0x!e-qm6k1%yoliec(15tn'

# Add your hosts to the list.
ALLOWED_HOSTS = ['127.0.0.1', 'office-crm.onrender.com', 'crm.power-devs.com']

# Database
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



EMAIL_HOST = '<specify host>'   # 'smtp.example.com'
EMAIL_HOST_PASSWORD = '<specify password>'
EMAIL_HOST_USER = 'crm@example.com'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = 'CRM: '
EMAIL_USE_TLS = True

SERVER_EMAIL = 'test@example.com'
DEFAULT_FROM_EMAIL = 'test@example.com'

ADMINS = [("<Admin1>", "<admin1_box@example.com>")]   # specify admin

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

FORMS_URLFIELD_ASSUME_HTTPS = True

# Internationalization
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('ar', 'Arabic'),
    ('cs', 'Czech'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('he', 'Hebrew'),
    ('hi', 'Hindi'),
    ('id', 'Indonesian'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('nl', 'Nederlands'),
    ('pl', 'Polish'),
    ('pt-br', 'Portuguese'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('vi', 'Vietnamese'),
    ('zh-hans', 'Chinese'),
]

TIME_ZONE = 'Asia/Karachi'   # specify your time zone

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LOGIN_URL = '/admin/login/'

# Application definition
INSTALLED_APPS = [
    "unfold",  # <--- important
    "unfold.contrib.filters",  # optional
    "unfold.contrib.forms",  # optional
    "unfold.contrib.inlines",  # optional
    "unfold.contrib.import_export",  # optional
    "unfold.contrib.guardian",  # optional
    "unfold.contrib.simple_history",  # optional
    "unfold.contrib.location_field",  # optional
    "unfold.contrib.constance",  # optional

    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crm.apps.CrmConfig',
    'massmail.apps.MassmailConfig',
    'analytics.apps.AnalyticsConfig',
    'help',
    'tasks.apps.TasksConfig',
    'chat.apps.ChatConfig',
    'voip',
    'common.apps.CommonConfig',
    'settings'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.utils.admin_redirect_middleware.AdminRedirectMiddleware',
    'common.utils.usermiddleware.UserMiddleware'
]

ROOT_URLCONF = 'webcrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webcrm.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    }
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

FIXTURE_DIRS = ['tests/fixtures']

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SITE_ID = 1

SECURE_HSTS_SECONDS = 0  # set to 31536000 for the production server
# Set all the following to True for the production server
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_PRELOAD = False
X_FRAME_OPTIONS = "SAMEORIGIN"

# ---- CRM settings ---- #

# For more security, replace the url prefixes
# with your own unique value.
SECRET_CRM_PREFIX = ''
SECRET_ADMIN_PREFIX = 'admin/'
SECRET_LOGIN_PREFIX = 'login/'

# Specify ip of host to avoid importing emails sent by CRM
CRM_IP = "127.0.0.1"

CRM_REPLY_TO = ["'Do not reply' <crm@example.com>"]

# List of addresses to which users are not allowed to send mail.
NOT_ALLOWED_EMAILS = []

# List of applications on the main page and in the left sidebar.
APP_ON_INDEX_PAGE = [
    'tasks', 'crm', 'analytics',
    'massmail', 'common', 'settings'
]
MODEL_ON_INDEX_PAGE = {
    'tasks': {
        'app_model_list': ['Task', 'Memo']
    },
    'crm': {
        'app_model_list': [
            'Request', 'Deal', 'Lead', 'Company',
            'CrmEmail', 'Payment', 'Shipment'
        ]
    },
    'analytics': {
        'app_model_list': [
            'IncomeStat', 'RequestStat'
        ]
    },
    'massmail': {
        'app_model_list': [
            'MailingOut', 'EmlMessage'
        ]
    },
    'common': {
        'app_model_list': [
            'UserProfile', 'Reminder'
        ]
    },
    'settings': {
        'app_model_list': [
            'PublicEmailDomain', 'StopPhrase'
        ]
    }
}

# Country VAT value
VAT = 0    # %

# 2-Step Verification Credentials for Google Accounts.
#  OAuth 2.0
CLIENT_ID = ''
CLIENT_SECRET = ''
OAUTH2_DATA = {
    'smtp.gmail.com': {
        'scope': "https://mail.google.com/",
        'accounts_base_url': 'https://accounts.google.com',
        'auth_command': 'o/oauth2/auth',
        'token_command': 'o/oauth2/token',
    }
}
# Hardcoded dummy redirect URI for non-web apps.
REDIRECT_URI = ''

# Credentials for Google reCAPTCHA.
GOOGLE_RECAPTCHA_SITE_KEY = ''
GOOGLE_RECAPTCHA_SECRET_KEY = ''

GEOIP = False
GEOIP_PATH = MEDIA_ROOT / 'geodb'

# For user profile list
SHOW_USER_CURRENT_TIME_ZONE = False

NO_NAME_STR = _('Untitled')

# For automated getting currency exchange rate
LOAD_EXCHANGE_RATE = False
LOADING_EXCHANGE_RATE_TIME = "6:30"
LOAD_RATE_BACKEND = ""  # "crm.backends.<specify_backend>.<specify_class>"

# Ability to mark payments through a representation
MARK_PAYMENTS_THROUGH_REP = False

# Site headers
SITE_TITLE = 'CRM'
ADMIN_HEADER = "ADMIN"
ADMIN_TITLE = "CRM Admin"
INDEX_TITLE = _('Main Menu')

# Allow mailing
MAILING = True

# This is copyright information. Please don't change it!
COPYRIGHT_STRING = f"Django-CRM. Copyright (c) {dt.now().year}"
PROJECT_NAME = "Django-CRM"
PROJECT_SITE = "https://djangocrm.github.io/info/"


TESTING = sys.argv[1:2] == ['test']
if TESTING:
    SECURE_SSL_REDIRECT = False
    LANGUAGE_CODE = 'en'
    LANGUAGES = [('en', ''), ('uk', '')]




# for local only remove in production
STATICFILES_DIRS = [
    BASE_DIR / "static_custom",
]



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
    "THEME": "light",  # or "light" / "dark"
    "BORDER_RADIUS": "8px",

    "STYLES": [
        lambda request: static("css/custom-forms.css"),
    ],

    # "STYLES": [
    #     lambda request: static("css/admin-extra.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/admin-extra.js"),
    # ],

    # SIDEBAR – keep this shape
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": True,   # hide auto-generated Django sidebar
        "navigation": [

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
            #             "link": "/en/admin/admin/logentry/",
            #             "actions": [
            #                 {
            #                     "title": "Add",
            #                     "icon": "add",
            #                     "link": "/en/admin/admin/logentry/add/",
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
            #             "link": "/en/admin/analytics/incomestat/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/admin/analytics/incomestat/add/"}
            #             ],
            #         },
            #         {
            #             "title": "IncomeStat Snapshots",
            #             "icon": "monitoring",
            #             "link": "/en/admin/analytics/incomestatsnapshot/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/admin/analytics/incomestatsnapshot/add/"}
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
            #             "link": "/en/admin/auth/group/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/admin/auth/group/add/"}
            #             ],
            #         },
            #         {
            #             "title": "Permissions",
            #             "icon": "lock",
            #             "link": "/en/admin/auth/permission/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/admin/auth/permission/add/"}
            #             ],
            #         },
            #         {
            #             "title": "Users",
            #             "icon": "person",
            #             "link": "/en/admin/auth/user/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/admin/auth/user/add/"}
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
            #             "link": "/en/admin/chat/chatmessage/",
            #             "actions": [
            #                 {"title": "Add", "icon": "add", "link": "/en/admin/chat/chatmessage/add/"}
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
            #         {"title": "Departments", "icon": "work", "link": "/en/admin/common/department/", "actions":[{"title":"Add","icon":"add","link":"/en/admin/common/department/add/"}]},
            #         {"title": "Files", "icon": "folder", "link": "/en/admin/common/thefile/", "actions":[{"title":"Add","icon":"add","link":"/en/admin/common/thefile/add/"}]},
            #         {"title": "Reminders", "icon": "alarm", "link": "/en/admin/common/reminder/", "actions":[{"title":"Add","icon":"add","link":"/en/admin/common/reminder/add/"}]},
            #         {"title": "User profiles", "icon": "badge", "link": "/en/admin/common/userprofile/", "actions":[{"title":"Add","icon":"add","link":"/en/admin/common/userprofile/add/"}]},
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
            #         {"title":"Cities","icon":"location_city","link":"/en/admin/crm/city/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/city/add/"}]},
            #         {"title":"Closing reasons","icon":"cancel","link":"/en/admin/crm/closingreason/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/closingreason/add/"}]},
            #         {"title":"Companies","icon":"business","link":"/en/admin/crm/company/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/company/add/"}]},
            #         {"title":"Contact persons","icon":"contacts","link":"/en/admin/crm/contact/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/contact/add/"}]},
            #         {"title":"Countries","icon":"public","link":"/en/admin/crm/country/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/country/add/"}]},
            #         {"title":"Currencies","icon":"payments","link":"/en/admin/crm/currency/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/currency/add/"}]},
            #         {"title":"Currency rates","icon":"trending_up","link":"/en/admin/crm/rate/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/rate/add/"}]},
            #         {"title":"Deals","icon":"handshake","link":"/en/admin/crm/deal/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/deal/add/"}]},
            #         {"title":"Emails in CRM","icon":"mail","link":"/en/admin/crm/crmemail/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/crmemail/add/"}]},
            #         {"title":"Industries of Clients","icon":"factory","link":"/en/admin/crm/industry/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/industry/add/"}]},
            #         {"title":"Lead Sources","icon":"source","link":"/en/admin/crm/leadsource/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/leadsource/add/"}]},
            #         {"title":"Leads","icon":"assignment","link":"/en/admin/crm/lead/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/lead/add/"}]},
            #         {"title":"Payments","icon":"attach_money","link":"/en/admin/crm/payment/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/payment/add/"}]},
            #         {"title":"Product categories","icon":"category","link":"/en/admin/crm/productcategory/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/productcategory/add/"}]},
            #         {"title":"Products","icon":"inventory","link":"/en/admin/crm/product/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/product/add/"}]},
            #         {"title":"Requests","icon":"help","link":"/en/admin/crm/request/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/request/add/"}]},
            #         {"title":"Shipments","icon":"local_shipping","link":"/en/admin/crm/shipment/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/shipment/add/"}]},
            #         {"title":"Stages","icon":"timeline","link":"/en/admin/crm/stage/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/stage/add/"}]},
            #         {"title":"Tags","icon":"sell","link":"/en/admin/crm/tag/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/tag/add/"}]},
            #         {"title":"Types of Clients","icon":"groups","link":"/en/admin/crm/clienttype/","actions":[{"title":"Add","icon":"add","link":"/en/admin/crm/clienttype/add/"}]},
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
            #         {"title":"Help pages","icon":"help_center","link":"/en/admin/help/page/","actions":[{"title":"Add","icon":"add","link":"/en/admin/help/page/add/"}]},
            #         {"title":"Paragraphs","icon":"description","link":"/en/admin/help/paragraph/","actions":[{"title":"Add","icon":"add","link":"/en/admin/help/paragraph/add/"}]},
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
                    {"title":"Email Accounts","icon":"alternate_email","link":"/en/admin/massmail/emailaccount/","actions":[{"title":"Add","icon":"add","link":"/en/admin/massmail/emailaccount/add/"}]},
                    {"title":"Email Messages","icon":"mail","link":"/en/admin/massmail/emlmessage/","actions":[{"title":"Add","icon":"add","link":"/en/admin/massmail/emlmessage/add/"}]},
                    {"title":"Eml accounts queues","icon":"queue","link":"/en/admin/massmail/emlaccountsqueue/","actions":[{"title":"Add","icon":"add","link":"/en/admin/massmail/emlaccountsqueue/add/"}]},
                    {"title":"Mailing Outs","icon":"outbox","link":"/en/admin/massmail/mailingout/","actions":[{"title":"Add","icon":"add","link":"/en/admin/massmail/mailingout/add/"}]},
                    {"title":"Mass contacts","icon":"people","link":"/en/admin/massmail/masscontact/","actions":[{"title":"Add","icon":"add","link":"/en/admin/massmail/masscontact/add/"}]},
                    {"title":"Signatures","icon":"draw","link":"/en/admin/massmail/signature/","actions":[{"title":"Add","icon":"add","link":"/en/admin/massmail/signature/add/"}]},
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
            #         {"title":"Banned company names","icon":"block","link":"/en/admin/settings/bannedcompanyname/","actions":[{"title":"Add","icon":"add","link":"/en/admin/settings/bannedcompanyname/add/"}]},
            #         {"title":"Massmail Settings","icon":"settings","link":"/en/admin/settings/massmailsettings/","actions":[{"title":"Add","icon":"add","link":"/en/admin/settings/massmailsettings/add/"}]},
            #         {"title":"Public email domains","icon":"public","link":"/en/admin/settings/publicemaildomain/","actions":[{"title":"Add","icon":"add","link":"/en/admin/settings/publicemaildomain/add/"}]},
            #         {"title":"Reminder settings","icon":"alarm_on","link":"/en/admin/settings/reminders/","actions":[{"title":"Add","icon":"add","link":"/en/admin/settings/reminders/add/"}]},
            #         {"title":"Stop Phrases","icon":"stop","link":"/en/admin/settings/stopphrase/","actions":[{"title":"Add","icon":"add","link":"/en/admin/settings/stopphrase/add/"}]},
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
            #         {"title":"Sites","icon":"language","link":"/en/admin/sites/site/","actions":[{"title":"Add","icon":"add","link":"/en/admin/sites/site/add/"}]},
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
            #         {"title":"Memos","icon":"sticky_note_2","link":"/en/admin/tasks/memo/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/memo/add/"}]},
            #         {"title":"Project stages","icon":"layers","link":"/en/admin/tasks/projectstage/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/projectstage/add/"}]},
            #         {"title":"Projects","icon":"folder_open","link":"/en/admin/tasks/project/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/project/add/"}]},
            #         {"title":"Resolutions","icon":"check_circle","link":"/en/admin/tasks/resolution/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/resolution/add/"}]},
            #         {"title":"Tags","icon":"sell","link":"/en/admin/tasks/tag/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/tag/add/"}]},
            #         {"title":"Task stages","icon":"timeline","link":"/en/admin/tasks/taskstage/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/taskstage/add/"}]},
            #         {"title":"Tasks","icon":"task","link":"/en/admin/tasks/task/","actions":[{"title":"Add","icon":"add","link":"/en/admin/tasks/task/add/"}]},
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
            #         {"title":"Connections","icon":"call","link":"/en/admin/voip/connection/","actions":[{"title":"Add","icon":"add","link":"/en/admin/voip/connection/add/"}]},
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
    #                 "link": "/en/admin/tasks/task/?status__exact=open",
    #                 "permission": "webcrm.settings.tabs_permission",
    #             },
    #             {
    #                 "title": _("Completed"),
    #                 "link": "/en/admin/tasks/task/?status__exact=done",
    #                 "permission": "webcrm.settings.tabs_permission",
    #             },
    #         ],
    #     },
    # ],
}


