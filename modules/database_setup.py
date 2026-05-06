import sqlite3
import os

def init_db():
    # Garante que a pasta data existe
    if not os.path.exists('data'):
        os.makedirs('data')
        
    conn = sqlite3.connect('data/agenda.db')
    cursor = conn.cursor()

    # Tabela de Veículos (Fiesta, Fox, etc)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            ano INTEGER,
            cor TEXT,
            placa TEXT,
            km_atual REAL DEFAULT 0
        )
    ''')

    # Tabela de Abastecimentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS abastecimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER,
            data TEXT,
            km_registro REAL,
            tipo_combustivel TEXT,
            litros REAL,
            valor_total REAL,
            media_abastecida REAL,
            FOREIGN KEY (veiculo_id) REFERENCES veiculos (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
