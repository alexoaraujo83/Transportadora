from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = [h.strip() for h in config('ALLOWED_HOSTS', default='*').split(',')]
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','rest_framework_simplejwt','django_filters','corsheaders','channels',
    'accounts','core','seguranca','clientes','precificacao','portal','inteligencia','fretes','motoristas','transportadoras','cotacoes','rastreamento','financeiro','notificacoes','relatorios','webhooks','integracoes','auditoria','operacoes'
]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware','django.middleware.security.SecurityMiddleware','seguranca.middleware.RateLimitMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','auditoria.middleware.AuditoriaMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
ASGI_APPLICATION='config.asgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':config('POSTGRES_DB', default='fusion_cargas'),'USER':config('POSTGRES_USER', default='fusion'),'PASSWORD':config('POSTGRES_PASSWORD', default='fusion123'),'HOST':config('POSTGRES_HOST', default='localhost'),'PORT':config('POSTGRES_PORT', default='5432')}}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='pt-br'; TIME_ZONE='America/Sao_Paulo'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; STATIC_ROOT=BASE_DIR/'staticfiles'; STATICFILES_DIRS=[BASE_DIR/'static'] if (BASE_DIR/'static').exists() else []
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='/accounts/login/'; LOGIN_REDIRECT_URL='/'; LOGOUT_REDIRECT_URL='/accounts/login/'
REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_FILTER_BACKENDS':['django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter','rest_framework.filters.OrderingFilter'],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':20,
}
# Preparado para cache/filas assíncronas
CACHES={'default':{'BACKEND':'django.core.cache.backends.locmem.LocMemCache','LOCATION':'fusion-cargas-cache'}}
CELERY_BROKER_URL=config('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND=config('CELERY_RESULT_BACKEND', default='redis://redis:6379/1')
CORS_ALLOW_ALL_ORIGINS=config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True
X_FRAME_OPTIONS='DENY'



# Segurança avançada - V7
RATE_LIMIT_WINDOW_SECONDS=config('RATE_LIMIT_WINDOW_SECONDS', default=60, cast=int)
RATE_LIMIT_LOGIN_PER_MINUTE=config('RATE_LIMIT_LOGIN_PER_MINUTE', default=5, cast=int)
RATE_LIMIT_API_PER_MINUTE=config('RATE_LIMIT_API_PER_MINUTE', default=120, cast=int)
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_REFERRER_POLICY='same-origin'
SESSION_COOKIE_SAMESITE='Lax'
CSRF_COOKIE_SAMESITE='Lax'
if not DEBUG:
    SECURE_SSL_REDIRECT=config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
    SECURE_HSTS_SECONDS=config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS=True
    SECURE_HSTS_PRELOAD=True


# Notificações em tempo real - V8
CHANNEL_LAYERS={
    'default':{
        'BACKEND':config('CHANNEL_LAYER_BACKEND', default='channels.layers.InMemoryChannelLayer'),
    }
}
