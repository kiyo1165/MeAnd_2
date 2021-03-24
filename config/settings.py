from pathlib import Path
import os
import environ
from django.contrib.messages import constants as messages
import datetime



MESSAGE_TAGS = {
    messages.DEBUG: 'dark',
    messages.ERROR: 'danger',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path( __file__ ).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0d4-ii#^@6v(s(!puzso105^twz24bs*!kc^@0usz=bhagxyqu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    'django.contrib.sites',
    'bootstrap4',
    'widget_tweaks',
    'django_cleanup',
    'main',
    'plan',
    'category',
    'message',
    'usercomments',
    'rest_framework',


    # 認証
    'allauth',
    'allauth.account',
    'accounts',
    # 画像編集
    'stdimage',
    # 決済
    'stripe',
    'checkout',
    # 予約
    'reservation',
    #follow
    'follow',
    #API
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '975864354045-62mmpdvb6ip7b4rgeb91ot4h8bvb7cqk.apps.googleusercontent.com',
            'secret': 'dv7XA4SaCkHb_doEaw47Smxp',
            'key': ''
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },

}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR, 'templates' ), os.path.join( BASE_DIR, 'templates', 'allauth' )],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [  # 追加
                'bootstrap4.templatetags.bootstrap4',
            ],
        },
    },
]
# django-environから環境変数を読み込む
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# env.SOCIAL_AUTH_FACEBOOK_KEY # アプリID
# env.SOCIAL_AUTH_FACEBOOK_SECRET  # app secret

ACCOUNT_FORMS = {
    'login': 'allauth.account.forms.LoginForm',
    'signup': 'allauth.account.forms.SignupForm',
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'meand_db3',
        'USER': 'kiyotsugu_akashi',  # os.environ.get( 'DB_USER' )
        'PASSWORD': 'kiyo1165',  # os.environ.get( 'DB_PASSWORD' )
        'HOST': '',
        'PORT': '',

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join( BASE_DIR, 'static' ),
)

MEDIA_ROOT = os.path.join( BASE_DIR, 'media' )
MEDIA_URL = '/media/'

# allauth設定
AUTH_USER_MODEL = 'accounts.User'
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    # 一般ユーザーのメール承認
    'allauth.account.auth_backends.AuthenticationBackend',
    # 管理サイト用（ユーザー名承認）
    'django.contrib.auth.backends.ModelBackend'
)

#emailデバック
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# メールアドレス承認に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

# サインアップにメールアドレス確認を挟むよう設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # 意味：必須
ACCOUNT_EMAIL_REQUIRED = True

# ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'accounts:mypage'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

# ソーシャルアカウント
SOCIALACCOUNT_AUTO_SIGNUP = True

#Stripe
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')

PUBLIC_HOLIDAYS = [

    # 2021
    datetime.date( year=2021, month=1, day=1 ),
    datetime.date( year=2021, month=1, day=11 ),
    datetime.date( year=2021, month=2, day=11 ),
    datetime.date( year=2021, month=2, day=23 ),
    datetime.date( year=2021, month=3, day=20 ),
    datetime.date( year=2021, month=4, day=29 ),
    datetime.date( year=2021, month=5, day=3 ),
    datetime.date( year=2021, month=5, day=4 ),
    datetime.date( year=2021, month=5, day=5 ),
    datetime.date( year=2021, month=7, day=19 ),
    datetime.date( year=2021, month=8, day=11 ),
    datetime.date( year=2021, month=9, day=20 ),
    datetime.date( year=2021, month=9, day=23 ),
    datetime.date( year=2021, month=10, day=11 ),
    datetime.date( year=2021, month=11, day=3 ),
    datetime.date( year=2021, month=11, day=23 ),
]
