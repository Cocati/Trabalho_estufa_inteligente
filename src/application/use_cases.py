from src.domain.entities import DadosAmbientais
from src.domain.protocols import (
    SensorGateway,
    DadosAmbientaisRepository,
    AtuadorGateway,
    NotificacaoGateway,
    LogGateway
)
from datetime import datetime
from typing import List, Dict

class ColetarDadosDoAmbienteUseCase:
    def __init__(
        self,
        sensor_gateway: SensorGateway,
        repositorio_de_dados: DadosAmbientaisRepository,
    ):
        self.sensor_gateway = sensor_gateway
        self.repositorio_de_dados = repositorio_de_dados

    def execute(self) -> DadosAmbientais:
        dados = self.sensor_gateway.coletar_dados()
        self.repositorio_de_dados.salvar(dados)
        print(f"Dados coletados e salvos: {dados}")
        return dados

class ControlarAmbienteUseCase:
    def __init__(
        self,
        sensor_gateway: SensorGateway,
        atuador_aquecedor: AtuadorGateway,
        log_gateway: LogGateway,
        temperatura_minima: float,
    ):
        self.sensor_gateway = sensor_gateway
        self.atuador_aquecedor = atuador_aquecedor
        self.log_gateway = log_gateway
        self.temperatura_minima = temperatura_minima

    def execute(self):
        dados = self.sensor_gateway.coletar_dados()
        
        if dados.temperatura < self.temperatura_minima:
            mensagem = "Aquecedor ligado. Temperatura abaixo do limite."
            self.atuador_aquecedor.ligar()
        else:
            mensagem = "Aquecedor desligado. Temperatura dentro do limite."
            self.atuador_aquecedor.desligar()
        
        self.log_gateway.registrar_evento(mensagem, str(datetime.now()))

class BuscarDadosParaMonitoramentoUseCase:
    def __init__(self, repositorio_de_dados: DadosAmbientaisRepository):
        self.repositorio_de_dados = repositorio_de_dados

    def execute(self) -> dict:
        dados = self.repositorio_de_dados.buscar_ultimo_dado()
        if dados:
            return {
                "temperatura": round(dados.temperatura, 2), # Formata aqui para duas casas
                "umidade": round(dados.umidade, 2),
                "luminosidade": round(dados.luminosidade, 2),
                "co2": round(dados.co2, 2)
            }
        return {
            "temperatura": "--",
            "umidade": "--",
            "luminosidade": "--",
            "co2": "--"
        }

    def execute_historico(self) -> List[Dict]:
        """Busca o histórico e o formata para a visualização."""
        historico = self.repositorio_de_dados.buscar_historico()
        
        return [
            {
                "temperatura": round(d.temperatura, 2), # Formata para duas casas
                "umidade": round(d.umidade, 2),
                "luminosidade": round(d.luminosidade, 2),
                "co2": round(d.co2, 2)
            }
            for d in historico
        ]

    def execute_media_diaria(self) -> List[Dict]:
        """Busca a média diária de dados ambientais."""
        return self.repositorio_de_dados.buscar_media_diaria()

class NotificarAnomaliaUseCase:
    def __init__(
        self,
        sensor_gateway: SensorGateway,
        notificacao_gateway: NotificacaoGateway,
        umidade_minima: float,
    ):
        self.sensor_gateway = sensor_gateway
        self.notificacao_gateway = notificacao_gateway
        self.umidade_minima = umidade_minima

    def execute(self):
        dados = self.sensor_gateway.coletar_dados()

        if dados.umidade < self.umidade_minima:
            mensagem = f"ALERTA: Umidade ({dados.umidade:.2f}%) está abaixo do limite ideal ({self.umidade_minima:.2f}%)!"
            print(f"Disparando alerta: {mensagem}")
            self.notificacao_gateway.enviar_alerta(mensagem)
