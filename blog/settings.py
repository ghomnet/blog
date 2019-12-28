"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

with open(os.path.join(BASE_DIR, 'settings.json'), encoding='utf-8') as f:
    settings_json = json.load(f)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_json['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings_json.get('DEBUG', False)
if DEBUG:
    ALLOWED_HOSTS = ['*', 'hao.stormsha.com']
else:
    ALLOWED_HOSTS = ['*', 'stormsha.com', 'www.stormsha.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',  # 添加人性化过滤器
    'storm',  # 博客应用
    'user',  # 自定义用户应用
    'comment',  # 评论
    'extend',
    'haystack',  # 全文搜索应用 这个要放在其他应用之前
    'rest_framework',  # API
    'compressor',  # 压缩js、css文件
    'mdeditor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'storm.context_processors.settings_info',  # 自定义上下文管理器
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# 添加 apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': settings_json['MYSQL_HOST'],
        'PORT': settings_json['MYSQL_PORT'],
        'USER': settings_json['MYSQL_USER'],
        'PASSWORD': settings_json['MYSQL_DB_PASSWORD'],
        'NAME': settings_json['MYSQL_NAME'],
        # 避免映射数据库时出现警告
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
# 使用django-redis缓存页面
REDIS_HOST = settings_json.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = settings_json.get('REDIS_PORT', '6379')
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}".format(REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 允许跨域访问
CORS_ORIGIN_ALLOW_ALL = True

# 开发环境时使用静态文件压缩
if DEBUG:
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True
else:
    DEBUG_PROPAGATE_EXCEPTIONS = True
# 静态文件收集
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'django.contrib.staticfiles.finders.FileSystemFinder',
                       'compressor.finders.CompressorFinder',)

# 静态文件路径
STATIC_URL = '/static/'
STATIC_ROOT = (
    os.path.join(BASE_DIR, 'static')
)

# 上传文件路径
MEDIA_URL = "/media/"  # 媒体文件别名(相对路径) 和 绝对路径
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media')
)

# 配置ck editor
MDEDITOR_UPLOAD_PATH = 'upload/'

# 公共资源路径
COMMON_DIR = os.path.join(BASE_DIR, "common")

# 日志
BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")

LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'simple'
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "blog_info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "blog_error.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "blog_collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {
       # 默认的logger应用如下配置
        '': {
            'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        # 名为 'collect'的logger还单独处理
        'collect': {
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        }
    },
}
# 统一分页设置
BASE_PAGE_BY = 4
BASE_ORPHANS = 5

# 全文搜索应用配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'storm.whoosh_cn_backend.WhooshEngine',  # 选择语言解析器为自己更换的结巴分词
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),  # 保存索引文件的地址，选择主目录下，这个会自动生成
    }
}
# 自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 自定义用户model
AUTH_USER_MODEL = 'user.Ouser'

SITE_DESCRIPTION = settings_json['SITE_DESCRIPTION']

SITE_KEYWORDS = settings_json['SITE_KEYWORDS']

SITE_END_TITLE = "聚会阅读器"

API_FLAG = settings_json['API_FLAG']

# 全局缓存时间
CACHE_TIME = settings_json['CACHE_TIME']

# 存放图片的主机
PIC_HOST = settings_json['PIC_HOST']
WEB_SITE = settings_json['WEB_SITE']

MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width
        'heigth': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                                                                                                           "emoji",
                    "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'upload',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True,  # Whether to open the sequence diagram function
        'watch': False,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False  # lineNumbers
    }
}

# 表情
SMILES = {
    "mrgreen": "mrgreen",
    "razz": "razz",
    "sad": "sad",
    "smile": "smile",
    "oops": "redface",
    "grin": "biggrin",
    "eek": "surprised",
    "???": "confused",
    "cool": "cool",
    "lol": "lol",
    "mad": "mad",
    "twisted": "twisted",
    "roll": "rolleyes",
    "wink": "wink",
    "idea": "idea",
    "arrow": "arrow",
    "neutral": "neutral",
    "cry": "cry",
    "?": "question",
    "evil": "evil",
    "shock": "eek",
    "!": "exclaim"
}

EMAIL_HOST = settings_json['EMAIL_HOST']  # 服务器
EMAIL_PORT = settings_json['EMAIL_PORT']  # 一般情况下都为25
EMAIL_HOST_USER = settings_json['EMAIL_HOST_USER']  # 账号
EMAIL_HOST_PASSWORD = settings_json['EMAIL_HOST_PASSWORD']  # 密码
EMAIL_USE_TLS = settings_json['EMAIL_USE_TLS']  # 一般都为False
# 打开ssl协议
EMAIL_USE_SSL = settings_json['EMAIL_USE_SSL']
EMAIL_FROM = settings_json['EMAIL_FROM']  # 邮箱来自

# 站点公共资源主机地址
COMMON_HOST = settings_json['COMMON_HOST']

# 微信公众平台ID、密码
APP_ID = settings_json['APP_ID']
APP_SECRET = settings_json['APP_SECRET']
APP_TOKEN = settings_json['APP_TOKEN']
