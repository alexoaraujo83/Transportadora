from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import dashboard
from core.health import healthcheck

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', dashboard, name='dashboard'),
    path('health/', healthcheck, name='healthcheck'),
    path('clientes/', include('clientes.urls')),
    path('precificacao/', include('precificacao.urls')),
    path('portal/', include('portal.urls')),
    path('inteligencia/', include('inteligencia.urls')),
    path('fretes/', include('fretes.urls')),
    path('motoristas/', include('motoristas.urls')),
    path('transportadoras/', include('transportadoras.urls')),
    path('cotacoes/', include('cotacoes.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('rastreamento/', include('rastreamento.urls')),
    path('notificacoes/', include('notificacoes.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('operacoes/', include('operacoes.urls')),
    path('webhooks/', include('webhooks.urls')),
    path('seguranca/', include('seguranca.urls')),
    path('api/v1/portal/', include('portal.api_urls')),
    path('api/v1/inteligencia/', include('inteligencia.api_urls')),
    path('api/v1/', include('core.api_urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
