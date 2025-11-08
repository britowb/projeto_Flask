# Checklist: Migrar de `db = SQLAlchemy(app)` → padrão Factory (`db = SQLAlchemy(); db.init_app(app)`)

Resumo: passos mínimos e verificados para refatorar a inicialização do SQLAlchemy usando o padrão factory, permitindo múltiplas instâncias da app, testes isolados e evitar import circulares.

---

## 1) Criar `extensions.py`
- Objetivo: declarar extensões desacopladas da app.
- Ação:
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

## 2) Converter a criação da app para factory
- Objetivo: criar instâncias da app com configs diferentes.
- Ação:
```python
import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db

load_dotenv()

def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///projeto.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)

    # registrar blueprints / comandos / inicializações aqui
    return app
```

---

## 3) Atualizar models para importar `db` de `extensions`
- Objetivo: evitar import circular e desacoplar models.
- Ação:
```python
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
```

---

## 4) Remover/alterar `db = SQLAlchemy(app)` no código atual
- Objetivo: garantir que não exista instância ligada ao app em módulos importados.
- Ação: comentar/remover instância direta do seu `config.py` ou similar.

---

## 5) Atualizar pontos que importavam `app` diretamente
- Procurar `from config import app` ou `from config import db`.
- Em scripts/CLI, criar app com:
```python
from app import create_app
app = create_app()
```

---

## 6) Inicialização do DB em contexto
- Para criar tabelas no desenvolvimento:
```python
with app.app_context():
    from extensions import db
    db.create_all()
```

---

## 7) Adaptação para testes (ex.: pytest)
- Fixture exemplo:
```python
import pytest
from app import create_app
from extensions import db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-key'
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

---

## 8) Se usar migrações: configurar Flask‑Migrate
- Instalar: `pip install Flask-Migrate`
- `extensions.py`:
```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
```
- `app.py`:
```python
from extensions import db, migrate
# após db.init_app(app):
migrate.init_app(app, db)
```
- Comandos:  
  - `flask db init`  
  - `flask db migrate -m "initial"`  
  - `flask db upgrade`  
  (Defina `FLASK_APP="app:create_app()"` conforme necessário)

---

## 9) Testar localmente
- Criar app dev e rodar:  
  `python -c "from app import create_app; create_app().run()"`
- Verificar endpoints e operações do DB.

---

## 10) Git / documentação
- Manter `.env` e `.venv` no `.gitignore`.
- Atualizar README com instruções: gerar `SECRET_KEY`, criar `.env`, ativar virtualenv, instalar `requirements.txt`, rodar migrações e testes.

---

## Notas importantes
- Ponto crítico: remover instância `db` ligada ao `app` em módulos que serão importados por models/blueprints.
- Migração incremental possível: primeiro criar `extensions.py` e atualizar models; depois mover `create_app` e remover `db = SQLAlchemy(app)`.
- Faça commit antes de começar para facilitar rollback.
