"""
Script de migration para adicionar a coluna 'solo' ao banco de dados.
Execute este script uma vez para atualizar o banco de dados existente.
"""

from database import engine
from sqlalchemy import text


def add_solo_column():
    """
    Adiciona a coluna 'solo' à tabela 'packets' se ela não existir.
    """
    with engine.connect() as conn:
        # Verificar se a coluna já existe
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='packets' AND column_name='solo'
        """)

        result = conn.execute(check_query)

        if result.fetchone():
            print("Coluna 'solo' já existe no banco de dados.")
            return

        # Adicionar a coluna 'solo'
        alter_query = text("""
            ALTER TABLE packets 
            ADD COLUMN solo FLOAT NOT NULL DEFAULT 0.0
        """)

        conn.execute(alter_query)
        conn.commit()
        print("Coluna 'solo' adicionada com sucesso ao banco de dados!")


if __name__ == "__main__":
    print("Executando migration para adicionar coluna 'solo'...")
    try:
        add_solo_column()
        print("Migration concluída!")
    except Exception as e:
        print(f"Erro ao executar migration: {e}")
