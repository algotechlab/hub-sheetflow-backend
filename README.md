# **hub-sheetflow-backend**

Backend responsável por realizar o **fluxo contínuo de dados** entre planilhas Excel e o sistema, garantindo ingestão, transformação, validação e sincronização de forma segura, modular e escalável.

---

## 📁 **Estrutura do Projeto**

A seguir, o mapa completo da estrutura atual do backend:


---

# 🧪 **Tecnologias utilizadas**

* **Python 3.13+**
* **Fastapi**
* **Alembic**
* **uvicorn**
* **Docker / Docker Compose**
* **Poetry**
* **Pytest**
* **Logging estruturado**
* **Arquitetura hexagonal**

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


# Comandos sobre a migração utilizando alembic


Este comando gera uma migração persistente ao banco de dados de acordo com o modelo que é codificado.

```
alembic revision --autogenerate -m ""
```