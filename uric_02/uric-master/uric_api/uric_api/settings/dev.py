"""
Django settings for uric_api project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR / 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+6plg@qo+pxdfu%(=pu7_rwjcy6#pvht)1*$+4k=^$ggrcuhs7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',  # 必须写在django.contrib.admin之前
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "home",
    'corsheaders',
    'users',
    'mtask',
    'consumer',
    "host",
    'channels',
    'conf_center',
    "release",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uric_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'uric_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "uric_user",
        "PASSWORD": "uric",
        "NAME": "uric",
    }
}

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

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日志配置
LOGGING = {
    # 使用的python内置的logging模块，那么python可能会对它进行升级，所以需要写一个版本号，目前就是1版本
    'version': 1,
    # #是否去掉目前项目中其他地方中以及使用的日志功能，但是将来我们可能会引入第三方的模块，里面可能内置了日志功能，所以尽量不要关闭，肯定False
    'disable_existing_loggers': False,
    # 日志的处理格式
    'formatters': {
        # 详细格式，往往用于记录日志到文件/其他第三方存储设备
        'verbose': {
            # levelname等级，asctime记录时间，module表示日志发生的文件名称，lineno行号，message错误信息
            'format': '{levelname} {asctime} {module}:{lineno:d} {message}',
            # 日志格式中的，变量分隔符
            'style': '{',
        },
        'simple': {  # 简单格式，往往用于终端
            'format': '{levelname} {module}:{lineno} {message}',
            'style': '{',
        },
    },
    'filters': {  # 日志的过滤设置，可以对日志进行输出时的过滤用的
        # 在debug=True下产生的一些日志信息，要不要记录日志，需要的话就在handlers中加上这个过滤器，不需要就不加
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志的处理方式
        'console': {  # 终端下显示
            'level': 'DEBUG',  # 日志的最低等级
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',  # 处理日志的核心类
            'formatter': 'simple'
        },
        'file': {  # 文件中记录日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': BASE_DIR.parent / "logs/uric.log",
            # 单个日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 备份日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 设置默认编码，否则打印出来汉字乱码
            'encoding': 'utf-8',
        },
    },
    # 日志实例对象
    'loggers': {
        'django': {  # 固定名称，将来django内部也会有异常的处理，只会调用django下标的日志对象
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# CORS组的配置信息
CORS_ORIGIN_WHITELIST = (
    # 'www.uric.cn:8080', # 如果这样写不行的话，就加上协议(http://www.uric.cn:8080，因为不同的corsheaders版本可能有不同的要求)
    'http://www.uric.cn:8082',
)
CORS_ALLOW_CREDENTIALS = False  # 是否允许ajax跨域请求时携带cookie，False表示不用，我们后面也用不到cookie，所以关掉它就可以了，以防有人通过cookie来搞我们的网站
ALLOWED_HOSTS = ["api.uric.cn", ]

REST_FRAMEWORK = {
    # 自定义异常处理
    'EXCEPTION_HANDLER': 'uric_api.utils.exceptions.custom_exception_handler',
    # 自定义认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # jwt认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # session认证
        'rest_framework.authentication.SessionAuthentication',

        'rest_framework.authentication.BasicAuthentication',
    ),
}

import datetime
JWT_AUTH = {
    # jwt的有效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=1),
    'JWT_ALLOW_REFRESH': True,
}

AUTH_USER_MODEL = 'users.User'

# 修改使用中文界面
LANGUAGE_CODE = 'zh-Hans'

# 修改时区
TIME_ZONE = 'Asia/Shanghai'

DEFAULT_KEY_NAME = "global"

# 配置channel的通道层
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # 需修改
        },
    },
}

# 在host应用下面创建一个routing.py文件
ASGI_APPLICATION = 'host.routing.application'

GIT_CODE_DIR = BASE_DIR.parent / 'projects'
