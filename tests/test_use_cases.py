import unittest
from src.application.use_cases import ColetarDadosDoAmbienteUseCase, ControlarAmbienteUseCase, NotificarAnomaliaUseCase
from src.domain.entities import DadosAmbientais
from tests.mocks.test_gateways import MockSensorGateway, SpyDadosAmbientaisRepository, AtuadorGatewayMock, NotificacaoGatewayMock, LogGatewaySpy
from datetime import datetime

class TestColetarDadosDoAmbienteUseCase(unittest.TestCase):
    def test_executar_deve_coletar_e_salvar_dados_ambientais(self):
        dados_esperados = DadosAmbientais(
            temperatura=26.0, umidade=88.5, luminosidade=250, co2=400,  timestamp=datetime.now() # O objeto datetime é passado aqui
        )
        mock_sensor = MockSensorGateway(dados_esperados)
        spy_repositorio = SpyDadosAmbientaisRepository()
        use_case = ColetarDadosDoAmbienteUseCase(mock_sensor, spy_repositorio)
        
        dados_obtidos = use_case.execute()

        self.assertEqual(dados_obtidos, dados_esperados)
        self.assertTrue(mock_sensor.chamada_coletar_dados)
        self.assertEqual(len(spy_repositorio.dados_salvos), 1)
        self.assertEqual(spy_repositorio.dados_salvos[0], dados_esperados)

class TestControlarAmbienteUseCase(unittest.TestCase):
    def test_deve_ligar_aquecedor_se_temperatura_estiver_abaixo_da_ideal(self):
        dados_baixa_temperatura = DadosAmbientais(
            temperatura=22.0, umidade=80.0, luminosidade=300, co2=450,  timestamp=datetime.now() # O objeto datetime é passado aqui
        )
        mock_sensor = MockSensorGateway(dados_baixa_temperatura)
        spy_aquecedor = AtuadorGatewayMock()
        spy_log = LogGatewaySpy()
        
        use_case = ControlarAmbienteUseCase(
            sensor_gateway=mock_sensor,
            atuador_aquecedor=spy_aquecedor,
            log_gateway=spy_log,
            temperatura_minima=24.0
        )
        
        use_case.execute()

        self.assertTrue(spy_aquecedor.estado_ligado)
        self.assertEqual(len(spy_log.eventos_registrados), 1)
        self.assertIn("ligado", spy_log.eventos_registrados[0]["evento"])

    def test_deve_desligar_aquecedor_se_temperatura_estiver_acima_da_ideal(self):
        dados_temperatura_ok = DadosAmbientais(
            temperatura=25.0, umidade=80.0, luminosidade=300, co2=450,  timestamp=datetime.now() # O objeto datetime é passado aqui
        )
        mock_sensor = MockSensorGateway(dados_temperatura_ok)
        spy_aquecedor = AtuadorGatewayMock()
        spy_log = LogGatewaySpy()

        use_case = ControlarAmbienteUseCase(
            sensor_gateway=mock_sensor,
            atuador_aquecedor=spy_aquecedor,
            log_gateway=spy_log,
            temperatura_minima=24.0
        )

        spy_aquecedor.ligar() # Pré-condição
        use_case.execute()
        
        self.assertFalse(spy_aquecedor.estado_ligado)
        self.assertEqual(len(spy_log.eventos_registrados), 1)
        self.assertIn("desligado", spy_log.eventos_registrados[0]["evento"])

class TestNotificarAnomaliaUseCase(unittest.TestCase):
    def test_deve_enviar_alerta_se_umidade_estiver_abaixo_da_minima(self):
        dados_baixa_umidade = DadosAmbientais(
            temperatura=25.0, umidade=75.0, luminosidade=300, co2=450,  timestamp=datetime.now() # O objeto datetime é passado aqui
        )
        mock_sensor = MockSensorGateway(dados_baixa_umidade)
        spy_notificacao = NotificacaoGatewayMock()

        use_case = NotificarAnomaliaUseCase(
            sensor_gateway=mock_sensor,
            notificacao_gateway=spy_notificacao,
            umidade_minima=80.0
        )
        
        use_case.execute()

        self.assertTrue(spy_notificacao.alerta_disparado)
        self.assertIn("Umidade", spy_notificacao.mensagem_enviada)

    def test_nao_deve_enviar_alerta_se_umidade_estiver_acima_da_minima(self):
        dados_umidade_ok = DadosAmbientais(
            temperatura=25.0, umidade=85.0, luminosidade=300, co2=450,  timestamp=datetime.now() # O objeto datetime é passado aqui
        )
        mock_sensor = MockSensorGateway(dados_umidade_ok)
        spy_notificacao = NotificacaoGatewayMock()
        
        use_case = NotificarAnomaliaUseCase(
            sensor_gateway=mock_sensor,
            notificacao_gateway=spy_notificacao,
            umidade_minima=80.0
        )

        use_case.execute()

        self.assertFalse(spy_notificacao.alerta_disparado)
        self.assertIsNone(spy_notificacao.mensagem_enviada)
