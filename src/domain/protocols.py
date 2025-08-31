from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime

from src.domain.entities import DadosAmbientais

class SensorGateway(ABC):
    @abstractmethod
    def coletar_dados(self) -> DadosAmbientais:
        pass

class DadosAmbientaisRepository(ABC):
    @abstractmethod
    def salvar(self, dados: DadosAmbientais):
        pass

    @abstractmethod
    def buscar_historico(self, periodo: datetime) -> List[DadosAmbientais]:
        pass

class AtuadorGateway(ABC):
    @abstractmethod
    def ligar(self):
        pass

    @abstractmethod
    def desligar(self):
        pass

class NotificacaoGateway(ABC):
    @abstractmethod
    def enviar_alerta(self, mensagem: str):
        pass

class LogGateway(ABC):
    @abstractmethod
    def registrar_evento(self, evento: str, timestamp: str):
        pass
