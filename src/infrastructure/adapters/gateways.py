from src.domain.entities import DadosAmbientais
from src.domain.protocols import SensorGateway, AtuadorGateway, LogGateway, NotificacaoGateway

class SensorHardwareAdapter(SensorGateway):
    def coletar_dados(self) -> DadosAmbientais:
        print("Lendo dados do hardware...")
        return DadosAmbientais(
            temperatura=25.5, umidade=85.0, luminosidade=300, co2=450
        )

class AtuadorHardwareAdapter(AtuadorGateway):
    def ligar(self):
        print("Ligando atuador físico...")

    def desligar(self):
        print("Desligando atuador físico...")
        
class FileLogAdapter(LogGateway):
    def __init__(self, log_path="log.txt"):
        self.log_path = log_path

    def registrar_evento(self, evento: str, timestamp: str):
        with open(self.log_path, "a") as f:
            f.write(f"[{timestamp}] - {evento}\n")
        print(f"Evento registrado em {self.log_path}: {evento}")

class EmailNotificacaoAdapter(NotificacaoGateway):
    def enviar_alerta(self, mensagem: str):
        print(f"Enviando e-mail de alerta: {mensagem}")
        # Lógica de envio de e-mail real
