# **hub-sheetflow-backend**

Backend responsável por realizar o **fluxo contínuo de dados** entre planilhas Excel e o sistema, garantindo ingestão, transformação, validação e sincronização de forma segura, modular e escalável.

---

## 📁 **Estrutura do Projeto**

A seguir, o mapa completo da estrutura atual do backend:

```
hub-sheetflow-backend/
├── CHANGES.md
├── Dockerfile
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose.yml
├── example.env
├── gunicorn.conf.py
├── manage.py
├── poetry.lock
├── pyproject.toml
├── tests/
│   └── ... (testes unitários)
└── src/
    ├── __init__.py
    ├── __pycache__/
    ├── auth/
    │   └── ... (módulos de autenticação, tokens, permissões)
    ├── core/
    │   └── ... (configurações gerais, logging, factory da aplicação)
    ├── db/
    │   ├── database.py   (instância do SQLAlchemy)
    │   ├── extensions.py (funções de conexão, inicialização, helpers)
    │   └── ...  
    ├── external.py       (clientes externos / integrações externas)
    ├── model/
    │   └── ... (modelos ORM do SQLAlchemy)
    ├── resource/
    │   └── ... (rotas e controladores da API — padrão Flask Resources)
    ├── service/
    │   └── ... (regras de negócio, casos de uso, validações)
    ├── static/
    │   └── ... (arquivos estáticos, se usados)
    └── utils/
        └── ... (funções utilitárias, helpers)
```

---

# 🧪 **Tecnologias utilizadas**

* **Python 3.12+**
* **Flask**
* **Flask-restx**
* **Flask-SQLAlchemy**
* **Alembic**
* **Gunicorn**
* **Docker / Docker Compose**
* **Poetry**
* **Pytest**
* **Logging estruturado**
* **Arquitetura modular (auth / service / resource / core)**

---

# 🚀 **Instalação e Setup**

### **1. Criar o arquivo `.env`**

```bash
cp example.env .env
```

Preencha as variáveis conforme seu ambiente.

---

### **2. Instalar o Poetry**

```bash
pip install poetry
```

---

### **3. Instalar dependências**

```bash
poetry install
```

---

## 🐳 **Executar o sistema com Docker**

### **Build da imagem**

```bash
docker compose build
```

### **Subir tudo**

```bash
docker compose up
```

A API ficará disponível na porta definida no `.env`.

---

# 🛠️ **Antes de fazer commit**

Execute os linters:

```bash
poetry run task format
poetry run task check
```

Rodar testes:

```bash
poetry run task test
```

---

# 🔧 **Gerenciar a aplicação**

Rodar comandos via `manage.py`:

```bash
poetry run python manage.py <comando>
```

Por exemplo, verificar conexão com DB, popular tabelas, rodar migrações, etc.

---

# 🗂️ **Padrão de arquitetura**

O projeto segue um padrão **orientado a camadas bem definidas**:

* **resource/** → Entrada da API (rotas, controllers)
* **service/** → Regras de negócio e casos de uso
* **model/** → Modelos ORM
* **db/** → Conexão, migrações e configurações do banco
* **core/** → Configuração global (factory, logging, middlewares)
* **utils/** → Funções utilitárias
* **auth/** → Login, tokens, permissões
