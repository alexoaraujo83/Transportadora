from decimal import Decimal
from django.utils import timezone
from .models import EventoRastreamento, PosicaoAtualFrete, PontoRota

class RastreamentoService:
    @staticmethod
    def registrar_posicao(frete, descricao='', latitude=None, longitude=None, velocidade_kmh=None, odometro_km=None, origem_evento='api'):
        evento=EventoRastreamento.objects.create(
            frete=frete, descricao=descricao or 'Posição atualizada', tipo=EventoRastreamento.TipoEvento.POSICAO,
            latitude=latitude, longitude=longitude, velocidade_kmh=velocidade_kmh, odometro_km=odometro_km, origem_evento=origem_evento
        )
        PosicaoAtualFrete.objects.update_or_create(
            frete=frete,
            defaults={'latitude':latitude,'longitude':longitude,'descricao':descricao,'velocidade_kmh':velocidade_kmh,'odometro_km':odometro_km}
        )
        return evento

    @staticmethod
    def concluir_ponto(ponto, descricao='Ponto concluído'):
        ponto.concluido=True
        ponto.realizado_em=timezone.now()
        ponto.save(update_fields=['concluido','realizado_em'])
        return EventoRastreamento.objects.create(
            frete=ponto.frete, descricao=f'{descricao}: {ponto.nome}', tipo=EventoRastreamento.TipoEvento.TRANSITO,
            latitude=ponto.latitude, longitude=ponto.longitude, origem_evento='rota'
        )

    @staticmethod
    def calcular_percentual_rota(frete):
        total=PontoRota.objects.filter(frete=frete).count()
        if not total:
            return 0
        feitos=PontoRota.objects.filter(frete=frete, concluido=True).count()
        return round((feitos/total)*100)

class MapasService:
    @staticmethod
    def gerar_link_google_maps(latitude, longitude):
        if latitude is None or longitude is None:
            return ''
        return f'https://www.google.com/maps?q={latitude},{longitude}'

    @staticmethod
    def gerar_link_rota(pontos):
        coords=[f'{p.latitude},{p.longitude}' for p in pontos if p.latitude is not None and p.longitude is not None]
        if len(coords) < 2:
            return ''
        origem=coords[0]; destino=coords[-1]; intermediarios='|'.join(coords[1:-1])
        base=f'https://www.google.com/maps/dir/?api=1&origin={origem}&destination={destino}'
        return base + (f'&waypoints={intermediarios}' if intermediarios else '')
