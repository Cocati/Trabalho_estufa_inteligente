from flask import Flask, jsonify, render_template, g
from src.infrastructure.adapters.controllers import ApiMonitoramentoController
from src.application.use_cases import (
    ColetarDadosDoAmbienteUseCase,
    ControlarAmbienteUseCase,
    BuscarDadosParaMonitoramentoUseCase,
    NotificarAnomaliaUseCase # Importar aqui
)
from src.infrastructure.adapters.gateways import (
    SensorHardwareAdapter,
    AtuadorHardwareAdapter,
    EmailNotificacaoAdapter,
    FileLogAdapter
)
from src.infrastructure.adapters.repositories import SQLiteRepositoryAdapter
import atexit

app = Flask(__name__)

def configure_dependencies():
    """Cria e retorna um novo conjunto de dependências."""
    sensor_gateway = SensorHardwareAdapter()
    atuador_gateway = AtuadorHardwareAdapter()
    notificacao_gateway = EmailNotificacaoAdapter()
    log_gateway = FileLogAdapter()
    repositorio_dados = SQLiteRepositoryAdapter() 

    coletar_dados_uc = ColetarDadosDoAmbienteUseCase(sensor_gateway, repositorio_dados)
    controlar_ambiente_uc = ControlarAmbienteUseCase(sensor_gateway, atuador_gateway, log_gateway, temperatura_minima=24.0)
    buscar_dados_uc = BuscarDadosParaMonitoramentoUseCase(repositorio_dados)
    notificar_anomalia_uc = NotificarAnomaliaUseCase(sensor_gateway, notificacao_gateway, umidade_minima=80.0)

    # Injetando todos os Use Cases necessários no controlador
    api_controller = ApiMonitoramentoController(
        coletar_dados_uc,
        controlar_ambiente_uc,
        buscar_dados_uc,
        notificar_anomalia_uc # Passar o use case de notificação aqui
    )
    return api_controller

@app.before_request
def setup_controller():
    g.api_controller = configure_dependencies()

@app.teardown_appcontext
def teardown_db(exception):
    db_adapter = getattr(g.api_controller.buscar_dados.repositorio_de_dados, 'conn', None)
    if db_adapter is not None:
        db_adapter.close()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    dados = g.api_controller.get_dados_ambiente()
    return jsonify(dados)

@app.route("/api/historico", methods=["GET"])
def get_historico():
    dados = g.api_controller.get_dados_historicos()
    return jsonify(dados)

@app.route("/api/historico/diario", methods=["GET"])
def get_historico_diario():
    dados = g.api_controller.get_dados_media_diaria()
    return jsonify(dados)

@app.route("/api/execute", methods=["POST"])
def execute_cycle():
    response = g.api_controller.post_coleta_e_controle()
    return jsonify(response)

@app.route("/api/anomalia", methods=["POST"])
def check_anomalia():
    response = g.api_controller.post_notificar_anomalia() # Chamar o novo método
    return jsonify(response)
