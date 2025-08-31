from datetime import datetime, timedelta
from src.infrastructure.adapters.repositories import SQLiteRepositoryAdapter
from src.domain.entities import DadosAmbientais
import random

def seed_data():
    """Popula o banco de dados com dados históricos de exemplo."""
    repo = SQLiteRepositoryAdapter(db_path="dados.db")
    
    # Adicionar dados de exemplo
    dados_historicos = [
        DadosAmbientais(
            temperatura=random.uniform(20.0, 26.0),
            umidade=random.uniform(75.0, 90.0),
            luminosidade=random.uniform(200.0, 400.0),
            co2=random.uniform(350.0, 500.0)
        )
        for _ in range(50)  # 50 pontos de dados
    ]
    
    for dados in dados_historicos:
        repo.salvar(dados)
    
    print("Massa de dados históricos gerada com sucesso!")

if __name__ == "__main__":
    seed_data()
