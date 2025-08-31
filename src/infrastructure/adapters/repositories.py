import sqlite3
from typing import List, Dict
from src.domain.entities import DadosAmbientais
from datetime import datetime
from config import DB_PATH # Importa o caminho do arquivo de configuração

class SQLiteRepositoryAdapter:
    def __init__(self, db_path=DB_PATH): # Altera o valor padrão
        self.db_path = db_path
        self.conn = None
        self.conectar()
        self.criar_tabela()

    def conectar(self):
        try:
            # Garante que o detector de threads seja desativado para o SQLite
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    
    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dados_ambientais (
                id INTEGER PRIMARY KEY,
                temperatura REAL,
                umidade REAL,
                luminosidade REAL,
                co2 REAL,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def salvar(self, dados: DadosAmbientais):
     cursor = self.conn.cursor()
     cursor.execute("""
        INSERT INTO dados_ambientais (temperatura, umidade, luminosidade, co2, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (dados.temperatura, dados.umidade, dados.luminosidade, dados.co2, dados.timestamp.isoformat()))
     self.conn.commit()
    
    def buscar_ultimo_dado(self) -> DadosAmbientais | None:
        """Busca e retorna o último registro de dados ambientais."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT temperatura, umidade, luminosidade, co2, timestamp FROM dados_ambientais ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return DadosAmbientais(
                temperatura=row[0],
                umidade=row[1],
                luminosidade=row[2],
                co2=row[3],
                timestamp=row[4]
            )
        return None

    def buscar_historico(self) -> List[DadosAmbientais]:
        """Busca todo o histórico de dados ambientais."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT temperatura, umidade, luminosidade, co2, timestamp FROM dados_ambientais ORDER BY timestamp ASC")
        rows = cursor.fetchall()
        
        historico = []
        for row in rows:
            historico.append(
                DadosAmbientais(
                    temperatura=row[0],
                    umidade=row[1],
                    luminosidade=row[2],
                    co2=row[3]
                )
            )
        return historico

    def buscar_media_diaria(self) -> List[Dict]:
        """Busca a média diária de temperatura, umidade, luminosidade e CO2."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                DATE(timestamp) as dia,
                AVG(temperatura) as media_temperatura,
                AVG(umidade) as media_umidade,
                AVG(luminosidade) as media_luminosidade,
                AVG(co2) as media_co2
            FROM dados_ambientais
            GROUP BY dia
            ORDER BY dia ASC
        """)
        rows = cursor.fetchall()
        
        medias_diarias = []
        for row in rows:
            medias_diarias.append({
                "dia": row[0],
                "temperatura": round(row[1], 2),
                "umidade": round(row[2], 2),
                "luminosidade": round(row[3], 2),
                "co2": round(row[4], 2)
            })
        return medias_diarias

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
