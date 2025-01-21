# LevelUp-rest-api
Projeto da disciplina de Reuso de Software. Trata-se de uma REST API utilizando o framework FastAPI do python consistindo em uma aplicação para persistir dados de cursos online.

# Migrações
- Inicialize o alembic: alembic init alembic
- No arquivo alembic.ini configure o sqlalchemy.url com as informações do bd. Ex.: postgresql://postgres:12345678@localhost:5432/levelup
- No arquivo env.py adicione SQLModel.metadata como valor da variável target_metadata
- No arquivo env.py importe os modelos. Ex.: from src.models import *
- Gere a migração: alembic revision --autogenerate -m "título da migração"
- Aplique as alterações ao banco de dados: alembic upgrade head

# Executando
- Criar um ambiente virtual com o seguinte comando: python -m venv .venv
- Rodar ambiente no prompt de comando do windows: .venv\Scripts\activate
- Instalar libs: pip install fastapi uvicorn sqlmodel psycopg2 alembic pyyaml
- Entrar na pasta src: cd src
- Executar o servidor com o seguinte comando: uvicorn main:app --reload