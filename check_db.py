import sqlite3
from config import DB_PATH

def check_data():
    """Conecta ao banco de dados e exibe os dados salvos."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Consulta para selecionar todos os dados da tabela
        cursor.execute("SELECT * FROM dados_ambientais")
        
        rows = cursor.fetchall()
        
        if not rows:
            print("Nenhum dado encontrado no banco de dados.")
            return

        print("Dados encontrados:")
        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_data()
