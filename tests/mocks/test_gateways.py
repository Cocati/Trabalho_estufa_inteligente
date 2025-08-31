from src.domain.entities import DadosAmbientais
from src.domain.protocols import (
    SensorGateway,
    DadosAmbientaisRepository,
    AtuadorGateway,
    NotificacaoGateway,
    LogGateway
)
from typing import List

class MockSensorGateway(SensorGateway):
    def __init__(self, dados_a_retornar: DadosAmbientais):
        self.dados_a_retornar = dados_a_retornar
        self.chamada_coletar_dados = False
    def coletar_dados(self) -> DadosAmbientais:
        self.chamada_coletar_dados = True
        return self.dados_a_retornar

class SpyDadosAmbientaisRepository(DadosAmbientaisRepository):
    def __init__(self):
        self.dados_salvos: List[DadosAmbientais] = []
    def salvar(self, dados: DadosAmbientais):
        self.dados_salvos.append(dados)
    def buscar_historico(self, periodo):
        return self.dados_salvos

class AtuadorGatewayMock(AtuadorGateway):
    def __init__(self):
        self.estado_ligado = False
    def ligar(self):
        self.estado_ligado = True
    def desligar(self):
        self.estado_ligado = False

class NotificacaoGatewayMock(NotificacaoGateway):
    def __init__(self):
        self.mensagem_enviada = None
        self.alerta_disparado = False
    def enviar_alerta(self, mensagem: str):
        self.mensagem_enviada = mensagem
        self.alerta_disparado = True

class LogGatewaySpy(LogGateway):
    def __init__(self):
        self.eventos_registrados = []
    def registrar_evento(self, evento: str, timestamp: str):
        self.eventos_registrados.append({"evento": evento, "timestamp": timestamp})
