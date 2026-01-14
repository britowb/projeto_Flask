Projeto PROJETO — Roadmap, Setup e Guia de Migrações

Este documento explica o estado atual do projeto, como criar ambientes distintos, usar a CLI do Flask para migrações, instalar dependências e manter o projeto numa rotina segura e reprodutível.

---

Resumo do estado atual
- A app já está organizada no padrão application factory com `create_app()` em `app.py`.
- As extensões `db` e `migrate` estão desacopladas em `extensions.py`.
- Existem classes de configuração por ambiente em `config.py` (`DevelopmentConfig`, `ProductionConfig`, `TestingConfig`).
- Os modelos estão em `models.py` e importam `db` de `extensions` (compatível com Flask-Migrate).
- Faltam: inicializar as migrações (`migrations/`), verificar dependências no venv e organizar scripts de desenvolvimento.

---

Objetivo deste README
- Servir como single source of truth sobre: instalação, seleção de ambientes, comandos de migração, testes e passos operacionais.
- Fornecer um pequeno roadmap de manutenção e checklist para deploys e desenvolvimentos futuros.

---

1) Requisitos e dependências
- Python 3.10+ (use virtualenv/venv)
- Dependências principais (instale no venv):

```bash
pip install -r requirements.txt
# ou, caso não tenha requirements.txt:
pip install Flask Flask-SQLAlchemy Flask-Migrate python-dotenv
```

Se você usa PowerShell no Windows:

```powershell
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

2) Estrutura relevante de arquivos
- `app.py` — application factory `create_app(config_name=None)`.
- `config.py` — classes `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`, e `config_by_name`.
- `extensions.py` — `db = SQLAlchemy()` e `migrate = Migrate()`.
- `models.py` — todos os modelos declarados usando `db` de `extensions`.
- `import secrets.py` — arquivo de testes/experimentos (mover ou renomear para `scripts/`).

---

3) Ambientes e seleção de configuração
Você pode selecionar a configuração de duas maneiras:

- Passando `config_name` ao chamar `create_app()` (por exemplo: `create_app('production')`).
- Ou definindo a variável de ambiente `FLASK_CONFIG` antes de executar comandos `flask`.

Valores válidos (conforme `config_by_name`): `development`, `production`, `testing`, `default`.

Exemplo (PowerShell):

```powershell
$env:FLASK_APP = "app:create_app()"
$env:FLASK_CONFIG = "development"
flask run
```

Exemplo (cmd.exe):

```cmd
set FLASK_APP=app:create_app()
set FLASK_CONFIG=development
flask run
```

Observação: no Windows, `setx` persiste variáveis, `set` / `$env:` apenas para a sessão atual.

---

4) CLI do Flask e Migrações (passo a passo)

1. Ative o ambiente virtual (venv)
2. Exporte/defina `FLASK_APP` e `FLASK_CONFIG` conforme mostrado acima
3. Inicialize as migrações (executar apenas uma vez por repositório):

```bash
flask db init
```

4. Gerar uma migration baseada nos modelos atuais:

```bash
flask db migrate -m "initial"
```

5. Aplicar a migration ao banco:

```bash
flask db upgrade
```

6. Fluxo para mudanças subsequentes de modelos:
   - Alterar `models.py`
   - `flask db migrate -m "describe change"`
   - `flask db upgrade`

Notas:
- Se `flask` reclamar sobre `FLASK_APP`, verifique que `FLASK_APP=app:create_app()` está corretamente definido.
- O `migrate` detecta modelos importados quando a app é criada; `app.py` já executa essas importações dentro da factory.

---

5) Testes e `TestingConfig`
- `TestingConfig` já está definida em `config.py` com `SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'`.
- Exemplo simples de fixture `pytest` (arquivo `tests/conftest.py`):

```python
import pytest
from app import create_app
from extensions import db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

Executar testes:

```bash
pytest -q
```

---

6) Organização de scripts e segurança
- Mova `import secrets.py` para `scripts/import_secrets.py` ou remova, para evitar execuções acidentais.
- Nunca commit um `.env` com `SECRET_KEY` ou credenciais; use `.env` local + `.gitignore`.

---

7) Rotina recomendada antes de commits/PRs
- Rodar linters/formatters (ex.: `black`, `flake8`).
- Rodar testes. Se alterações no DB, criar migration e rodar `flask db upgrade` localmente.
- Atualizar `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

8) Troubleshooting rápido
- Erro: `flask: command not found` — ative o venv e confirme `pip install Flask`.
- Erro: `Can't locate Flask application` — verifique `FLASK_APP` apontando para `app:create_app()`.
- Migrações vazias — confirme se os modelos são importados quando a app é criada; `app.py` já executa essas importações dentro de `create_app()`.

---

9) Roadmap / Próximos passos (curto e médio prazo)
- Curto (agora):
  - Verificar/instalar dependências no venv.
  - Mover/remover `import secrets.py` para `scripts/`.
  - Rodar `flask db init` e gerar a migration inicial.
- Médio:
  - Criar `tests/` com cobertura básica (autenticação, CRUD para modelos principais).
  - Preparar `docker-compose` (opcional) com Postgres para dev/prod parity.
  - Adicionar CI que rode `pytest` e aplique migrations num banco temporário.
- Longo:
  - Estratégia de deploy: manter migrates no pipeline; criar script de deploy que aplica `flask db upgrade` antes de reiniciar serviços.

---

Se você quiser, eu já:
- verifico/instalo as dependências no seu ambiente virtual e inicio as migrações, ou
- movo `import secrets.py` para `scripts/` agora.

Caso queira que eu execute alguma dessas ações agora, diga qual opção prefere.
