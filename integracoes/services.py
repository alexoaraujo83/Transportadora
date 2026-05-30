class WhatsAppService:
    """Preparação para integração com WhatsApp oficial/Twilio/Z-API.
    Configure a chave no .env e substitua o retorno simulado pela chamada HTTP real.
    """
    def enviar_mensagem(self, telefone: str, mensagem: str) -> dict:
        return {'simulado': True, 'telefone': telefone, 'mensagem': mensagem}

class GerenciadoraRiscoService:
    """Interface preparada para consulta externa de risco do motorista."""
    def consultar_motorista(self, cpf: str, placa: str = '') -> dict:
        return {'cpf': cpf, 'placa': placa, 'status': 'PENDENTE_INTEGRACAO'}

class MapaService:
    """Interface para cálculo de rota e geocodificação."""
    def calcular_rota(self, origem: str, destino: str) -> dict:
        return {'origem': origem, 'destino': destino, 'distancia_km': None, 'status': 'PENDENTE_INTEGRACAO'}
