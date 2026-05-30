from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import EventoSeguranca, PoliticaAcesso

def staff_required(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(staff_required)
def painel_seguranca(request):
    eventos = EventoSeguranca.objects.select_related('usuario')[:100]
    politicas = PoliticaAcesso.objects.all().order_by('perfil','modulo')[:200]
    criticos = EventoSeguranca.objects.filter(severidade__in=['ALTA','CRITICA']).count()
    return render(request, 'seguranca/painel.html', {'eventos': eventos, 'politicas': politicas, 'criticos': criticos})
