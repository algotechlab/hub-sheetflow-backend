# **hub-sheetflow-backend**

Backend responsável por orquestrar o **fluxo contínuo de dados** entre planilhas Excel e o sistema interno. Ele realiza **ingestão, transformação, validação e sincronização** de forma segura, modular e escalável, seguindo princípios de *Clean Architecture* e uma abordagem hexagonal.

---

## 📁 **Estrutura do Projeto**

```textplain
hub-sheetflow-backend/
├── entrypoints/                    # Scripts de entrada dos containers Docker
│   └── init-app.sh                # Inicialização da aplicação dentro do container
│
├── pipelines/                      # Configurações de CI/CD
│   └── app-python.yaml            # Pipeline de build/deploy
│
├── .vscode/                        # Configurações do VSCode
│   ├── launch.json                # Debug com Docker
│   └── settings.json              # Ajustes personalizados
│
├── src/                            # Código-fonte principal
│   ├── application/               # Camada de aplicação
│   │   └── api/
│   │       └── v1/
│   │           ├── controllers/   # Processamento de requisições
│   │           ├── middlewares/   # Interceptadores de requisição
│   │           ├── routes/        # Definição das rotas
│   │           ├── schemas/       # Validação e contratos de entrada/saída
│   │           └── __init__.py
│   │
│   ├── core/                      # Regras de domínio
│   │   ├── config/                # Configurações globais
│   │   ├── domain/                # Entidades e lógica de domínio
│   │   │   ├── exceptions/        # Exceções de domínio
│   │   │   ├── interfaces/        # Interfaces de repositórios
│   │   │   ├── services/          # Serviços principais
│   │   │   ├── use_cases/         # Casos de uso
│   │   │   └── __init__.py
│   │   └── exceptions/            # Exceções globais da aplicação
│   │
│   ├── infrastructure/            # Infraestrutura e persistência
│   │   ├── repositories/          # Implementações concretas de repositórios
│   │   └── __init__.py
│   │
│   └── main.py                    # Ponto de entrada principal da API
│
├── tests/                          # Testes automatizados
│   └── unit/
│       ├── application/
│       ├── core/
│       ├── infrastructure/
│       └── test_main.py
│
├── Dockerfile                      # Build da imagem Docker
├── docker-compose.yml              # Orquestração local
├── pyproject.toml                  # Dependências via Poetry
└── README.md                       # Documentação do projeto
```

---

## 🔧 **Tecnologias utilizadas**

* Python **3.13+**
* **FastAPI**
* **SQLAlchemy**
* **Alembic**
* **Uvicorn**
* **Docker & Docker Compose**
* **Poetry**
* **Pytest**
* **Logging estruturado**
* **Arquitetura Hexagonal**

---

# 🚀 **Instalação e Setup**

## 1️⃣ Criar o arquivo `.env`

```bash
cp example.env .env
```

Preencha as variáveis conforme o seu ambiente local.

---

## 2️⃣ Instalar o Poetry

```bash
pip install poetry
```

---

## 3️⃣ Instalar dependências

```bash
poetry install
```

---

# 🐳 **Executar com Docker**

## 🔨 Build da imagem

```bash
docker compose build
```

## ▶️ Subir o ambiente

```bash
docker compose up
```

A API ficará disponível na porta configurada no `.env`.

---

# 🛠️ **Fluxo de desenvolvimento**

Antes de commitar, execute:

### Formatadores:

```bash
poetry run task format
poetry run task check
```

### Testes:

```bash
poetry run task test
```

---

# ⚙️ **Rodar manualmente (modo desenvolvimento)**

Para iniciar com debug ativo:

```bash
make run
```

Isso executa:

```
python -m debugpy --listen 0.0.0.0:5678 -m uvicorn src.main:app --reload --workers 3 --host 0.0.0.0 --port 8000
```

---

# 🗂️ **Padrão de arquitetura**

O projeto segue uma arquitetura **orientada a domínio**, com camadas isoladas:

| Camada            | Descrição                                                    |
| ----------------- | ------------------------------------------------------------ |
| `application/`    | Camada de entrada: controllers, rotas, middlewares e schemas |
| `core/`           | Regras de negócio, entidades, casos de uso, serviços         |
| `infrastructure/` | Banco de dados, repositórios, integrações externas           |
| `migrations/`     | Controle de migrações usando Alembic                         |

---

# 🧬 **Migrações (Alembic)**

Gerar uma nova migração com base nas models:

```bash
alembic revision --autogenerate -m "mensagem da migração"
```

Aplicar migrações:

```bash
alembic upgrade head
```

Reverter:

```bash
alembic downgrade -1
```

---

# 🤝 **Contribuindo**

1. Crie uma branch a partir da `main`
2. Execute `task format` e `task check`
3. Adicione ou atualize testes
4. Abra um Pull Request bem documentado

---

# 📄 **Licença**

Este projeto é privado e de uso interno.

---