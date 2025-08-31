import os
from src.infrastructure.adapters.repositories import SQLiteRepositoryAdapter
from src.domain.entities import DadosAmbientais
import random
from datetime import datetime, timedelta
from config import DB_PATH

def seed_data(num_records=50):
    """Popula o banco de dados com dados históricos de exemplo."""
    try:
        repo = SQLiteRepositoryAdapter(db_path=DB_PATH)

        # Gera dados para 50 dias diferentes
        for i in range(num_records):
            # O timestamp agora é de um dia diferente, no passado
            timestamp_anterior = datetime.now() - timedelta(days=num_records - 1 - i)
            dados = DadosAmbientais(
                temperatura=random.uniform(20.0, 26.0),
                umidade=random.uniform(75.0, 90.0),
                luminosidade=random.uniform(200.0, 400.0),
                co2=random.uniform(350.0, 500.0),
                timestamp=timestamp_anterior # Passa o timestamp para a entidade
            )
            repo.salvar(dados)

        print(f"Massa de dados históricos ({num_records} registros) gerada com sucesso!")

    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")

    finally:
        if repo.conn:
            repo.conn.close()

def reset_db():
    """Deleta o banco de dados e recria-o com dados de exemplo."""
    db_file = DB_PATH
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Banco de dados '{db_file}' deletado.")
    else:
        print(f"Banco de dados '{db_file}' não encontrado, criando um novo.")

    seed_data()

if __name__ == "__main__":
    print("Iniciando o processo de reset e recarga do banco de dados...")
    reset_db()
    print("Processo concluído.")