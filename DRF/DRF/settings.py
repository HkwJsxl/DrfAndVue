"""
Django settings for DRF project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-23kjg(sus@x3g2u&9crh$@5vw!f(-%ky2io*!ga1sa^lc!4f@+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'django_filters',
    'sub_apps.version_manage.apps.VersionManageConfig',
    'sub_apps.auth_permission.apps.AuthPermissionConfig',
    'sub_apps.access_frequency.apps.AccessFrequencyConfig',
    'sub_apps.serializer_related.apps.SerializerRelatedConfig',
    'sub_apps.views_related.apps.ViewsRelatedConfig',
    'sub_apps.exception_response.apps.ExceptionResponseConfig',
    'sub_apps.practice.apps.PracticeConfig',
    'rest_framework_swagger',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DRF.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = "DRF.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"
# LANGUAGE_CODE = "zh-hans"  # 语言更改为汉字（数据校验错误信息...）

TIME_ZONE = "UTC"

USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "VERSION_PARAM": "version",  # url传参时,指定版本的key
    "DEFAULT_VERSION": "v1",  # 版本的默认值
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],  # 允许的版本号
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning",  # 全局配置

    # "UNAUTHENTICATED_USER": lambda: None,  # 认证返回值
    # "UNAUTHENTICATED_TOKEN": lambda: None,
    # "DEFAULT_AUTHENTICATION_CLASSES": ['utils.auth_related.TokenAuthentication', ]  # 全局配置
    # "DEFAULT_PERMISSION_CLASSES": ["utils.permission_related.RolePermission", ]

    # "DEFAULT_THROTTLE_CLASSES": ["utils.throttle_related.RateThrottle", ],  # 全局配置
    # "DEFAULT_THROTTLE_RATES": {
    #     "user_access": "10/m",
    # }

    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', ]  # 筛选
    # 'PAGE_SIZE': 2,  # 分页

    # 'EXCEPTION_HANDLER': 'utils.exception_response.re_exception_handler',  # 异常处理

    # 接口文档-coreapi
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456",
        }
    }
}
