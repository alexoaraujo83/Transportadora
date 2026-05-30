from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notificacao

@login_required
def central_notificacoes(request):
    notificacoes=Notificacao.objects.filter(usuario=request.user)[:100]
    nao_lidas=Notificacao.objects.filter(usuario=request.user,lida=False).count()
    return render(request,'notificacoes/central.html',{'notificacoes':notificacoes,'nao_lidas':nao_lidas})
