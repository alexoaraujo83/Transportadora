from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TokenExterno, AceiteDigitalFrete, ComprovantePortal

def consulta_frete(request, token):
    token_obj=get_object_or_404(TokenExterno, token=token, ativo=True)
    frete=token_obj.frete
    timeline=list(frete.rastreamentos.all().order_by('-criado_em')[:20]) if hasattr(frete, 'rastreamentos') else []
    return render(request,'portal/consulta_frete.html',{'frete':frete,'token_obj':token_obj,'timeline':timeline})

def aceitar_frete(request, token):
    token_obj=get_object_or_404(TokenExterno, token=token, ativo=True)
    if request.method=='POST':
        AceiteDigitalFrete.objects.create(
            frete=token_obj.frete,
            nome=request.POST.get('nome',''),
            documento=request.POST.get('documento',''),
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT','')[:1000],
        )
        messages.success(request,'Aceite digital registrado com sucesso.')
        return redirect('portal_consulta_frete', token=token)
    return render(request,'portal/aceitar_frete.html',{'frete':token_obj.frete,'token_obj':token_obj})

def enviar_comprovante(request, token):
    token_obj=get_object_or_404(TokenExterno, token=token, ativo=True)
    if request.method=='POST':
        ComprovantePortal.objects.create(
            frete=token_obj.frete,
            tipo=request.POST.get('tipo','OUTRO'),
            descricao=request.POST.get('descricao',''),
            arquivo=request.FILES.get('arquivo')
        )
        messages.success(request,'Comprovante recebido.')
        return redirect('portal_consulta_frete', token=token)
    return render(request,'portal/enviar_comprovante.html',{'frete':token_obj.frete,'token_obj':token_obj})
