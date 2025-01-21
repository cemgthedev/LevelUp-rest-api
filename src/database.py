from sqlmodel import SQLModel, Session, create_engine
from models import *

# Configuração da URL do banco de dados
DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/levelup"

# Criação do engine
engine = create_engine(DATABASE_URL)

# Criação das tabelas no banco de dados
def create_tables():
    try:
        SQLModel.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

# Executar a criação das tabelas
create_tables()

# Função para obter uma sessão de banco de dados
def get_db():
    with Session(engine) as session:
        yield session