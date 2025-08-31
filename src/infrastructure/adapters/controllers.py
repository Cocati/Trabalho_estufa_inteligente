from src.application.use_cases import (
    ColetarDadosDoAmbienteUseCase,
    ControlarAmbienteUseCase,
    BuscarDadosParaMonitoramentoUseCase,
    NotificarAnomaliaUseCase # Importar NotificarAnomaliaUseCase
)
from typing import List, Dict

class ApiMonitoramentoController:
    def __init__(
        self,
        coletar_dados_use_case: ColetarDadosDoAmbienteUseCase,
        controlar_ambiente_use_case: ControlarAmbienteUseCase,
        buscar_dados_use_case: BuscarDadosParaMonitoramentoUseCase,
        # Adicionar o use case de notificação no construtor
        notificar_anomalia_uc: NotificarAnomaliaUseCase 
    ):
        self.coletar_dados = coletar_dados_use_case
        self.controlar_ambiente = controlar_ambiente_use_case
        self.buscar_dados = buscar_dados_use_case
        self.notificar_anomalia_uc = notificar_anomalia_uc # Atribuir aqui

    def get_dados_ambiente(self):
        return self.buscar_dados.execute()

    def get_dados_historicos(self) -> List[Dict]:
        return self.buscar_dados.execute_historico()

    def get_dados_media_diaria(self) -> List[Dict]:
        """Retorna os dados da média diária."""
        return self.buscar_dados.execute_media_diaria()

    def post_coleta_e_controle(self):
        self.coletar_dados.execute()
        self.controlar_ambiente.execute()
        return {"status": "Ação de coleta e controle executada com sucesso!"}

    def post_notificar_anomalia(self): # Novo método para a rota de anomalia
        self.notificar_anomalia_uc.execute()
        return {"status": "Verificação de anomalia executada."}
