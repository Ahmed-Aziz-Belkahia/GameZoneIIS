from django.contrib.messages import constants as messages
from pathlib import Path
from datetime import timedelta
import os
import environ
import dj_database_url

env = environ.Env()
environ.Env.read_env()

# company = Company.objects.all().first()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "env('SECRET_KEY')"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Custom
    'store',
    'core',
    'addons',
    'userauths',
    'vendor',
    'reports',
    'blog',
    'help_center',

    # Third Party
    'import_export',
    'crispy_forms',
    'mathfilters',
    'ckeditor',
    'ckeditor_uploader',
    'django_ckeditor_5',
    'taggit',
    "anymail",
    'paypal.standard.ipn',
    'geoip2',
    'django_user_agents',
    'django_extensions',
    # 'captcha',
    'storages',
    'crispy_bootstrap5',

]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'ecommerce_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'core.context_processor.default',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_prj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': env("ENGINE"),
#         'NAME': env("NAME"),
#         'USER': env("USER"),
#         'PASSWORD': env("PASSWORD"),
#         'HOST': env("HOST"),
#         'PORT': env("PORT"),
#     }
# }

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")

# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

# AWS_S3_FILE_OVERWRITE = False

# AWS_DEFAULT_ACL = None

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# AWS_LOCATION = 'static'

# STATIC_LOCATION = 'static'

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "userauths:sign-in"

LOGIN_REDIRECT_URL = ""

LOGOUT_REDIRECT_URL = "userauths:sign-in"

AUTH_USER_MODEL = 'userauths.User'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240


STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_CONNECT_CLIENT_ID = env("STRIPE_CONNECT_CLIENT_ID")

PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID")
PAYPAL_SECRET_ID = env("PAYPAL_SECRET_ID")

PAYPAL_RECEIVER_EMAIL =  env("PAYPAL_RECEIVER_EMAIL")
PAYPAL_TEST = env("PAYPAL_TEST")
PAYPAL_ACCESS_TOKEN = os.environ.get("PAYPAL_ACCESS_TOKEN")

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN"),  
}



""" FROM_EMAIL='contact@gameszone.tn'
EMAIL_BACKEND='anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL='contact@gameszone.tn'
SERVER_EMAIL='contact@gameszone.tn' """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ahmadazizbelkahiag2a@gmail.com'
EMAIL_HOST_PASSWORD='rjsz fsvm yrgm eizg'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

GEOIP_PATH =os.path.join('geoip')

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        'skin': 'moono',
        "codeSnippet_theme": 'monokai',
        "toolbar": "all",
        "extraPlugins": ','.join([
            "codesnippet",
            "widget",
            "dialog",
        ])
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "mediaEmbed": {"previewsInData": "true"},
        "language": "en",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "codeBlock",
            "numberedList",
            "todoList",
            "|",
            "outdent",
            "indent",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
    },
}

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 10 MB


JAZZMIN_SETTINGS = {
    'site_header': "GameZone",
    'site_brand': "Game Zone, le premier spécialiste en consoles et machines de jeux en Tunisie ! Découvrez notre large gamme de produits, incluant les consoles PlayStation 4, PlayStation 5, Nintendo Switch et Xbox. Nous offrons également des services de réparation pour vos appareils. Plongez dans l'univers du jeu avec Game Zone dès aujourd'hui !",
    'site_logo': "images/logo.png",
    'copyright':  "All Right Reserved 2024",
    # "order_with_respect_to": ["store", 'vendor', "addons" , 'core' ,'userauths'],
    "welcome_sign": "Welcome to GameZone, Login Now.",
    "topmenu_links": [

        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Company", "url": "/admin/addons/company/"},
        {"name": "Users", "url": "/admin/userauths/user/"},

        # model admin to link to (Permissions checked against model)
        {"model": "AUTH_USER_MODEL.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"store": "Product"},
    ],

    # "order_with_respect_to": ["store", "store.Product"],

    "order_with_respect_to": [
        "store",
        "store.product",
        "store.cartorder",
        "store.cartorderitem",
        "store.category",
        "store.brand",
        "store.productfaq",
        "store.productoffers",
        "store.productbidders",
        "store.review",
        "vendor",
        "userauths"
        "addons",
        "addons.company"
    ],
    
    "icons": {
        "admin.LogEntry": "fas fa-file",

        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",

        "userauths.User": "fas fa-user",
        "userauths.Profile":"fas fa-address-card",

        "store.Product": "fas fa-th",
        "store.CartOrder":"fas fa-shopping-cart",
        "store.CartOrderItem":"fas fa-shopping-basket",
        "store.Brand":"fas fa-check-circle",
        "store.productfaq":"fas fa-question",
        "store.productoffers":"fas fa-handshake",
        "store.productbidders":"fas fa-poll",
        "store.Review":"fas fa-star fa-beat",
        "store.Category":"fas fa-tag",

        "vendor.Vendor":"fas fa-store",
        "vendor.Coupon":"fas fa-percentage",
        "vendor.DeliveryCouriers":"fas fa-truck",
        "vendor.Notification":"fas fa-bell",
        "vendor.PayoutTracker":"fas fa-wallet",
        "vendor.ChatMessage":"fas fa-envelope",


        "addons.AboutUS":"fas fa-users",
        "addons.Company":"fas fa-university",
        "addons.BasicAddon":"fas fa-cog",
        "addons.NewsLetter":"fas fa-envelope",
        "addons.Policy":"fas fa-copyright",
        "addons.ContactUs":"fas fa-phone",
        "addons.Announcements":"fas fa-microphone",
        "addons.PlatformNotifications":"fas fa-bell",
        "addons.SupportContactInformation":"fas fa-headset",
        "addons.TaxRate":"fas fa-percentage",
        "addons.HomePageSetup":"fas fa-home",
        "addons.FAQs":"fas fa-question",
        "addons.PaymentMethod":"fas fa-credit-card",


        "blog.Post":"fas fa-th",
        "blog.Category":"fas fa-tag",
        "blog.Comment":"fas fa-comments",

        "core.Address":"fas fa-map-marker",
        "core.BillingAddress":"fas fa-credit-card",
        "core.CancelledOrder":"fas fa-ban",
        "core.Wishlist":"fas fa-heart",
        "store.CallToActionBanner":"fas fa-solid fa-images",
        "store.Genre":"fas fa-solid fa-bookmark",
        "store.SpecificationValue":"fas fa-solid fa-table",
        "store.Specification":"fas fa-solid fa-border-none",
        "store.SubCategory":"fas fa-solid fa-layer-group",
        "store.Type":"fas fa-solid fa-database",

        
    },


    "show_ui_builder" : True
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-olive",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}