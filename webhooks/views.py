from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import WebhookEvento

@method_decorator(csrf_exempt, name='dispatch')
class WebhookReceiverView(View):
    def post(self, request, origem='externo'):
        try: payload=json.loads(request.body.decode() or '{}')
        except json.JSONDecodeError: payload={'raw': request.body.decode(errors='ignore')}
        evento=payload.get('evento') or payload.get('event') or 'evento_recebido'
        obj=WebhookEvento.objects.create(origem=origem, evento=evento, payload=payload)
        return JsonResponse({'ok': True, 'id': obj.id})
