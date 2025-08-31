import dataclasses
from datetime import datetime

@dataclasses.dataclass
class DadosAmbientais:
    temperatura: float
    umidade: float
    luminosidade: float
    co2: float
    timestamp: datetime
