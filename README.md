# NoSQL Neo4j Example (FastAPI)

Exemplo simples de um CRUD (Persons, Companies) em Neo4j usando FastAPI.

Endpoints principais:
- POST /persons
- GET /persons
- GET /persons/{person_id}
- PUT /persons/{person_id}
- DELETE /persons/{person_id}

- POST /companies
- GET /companies
- GET /companies/{company_id}
- PUT /companies/{company_id}
- DELETE /companies/{company_id}

- POST /relationships (cria relação WORKS_AT entre Person e Company)
- DELETE /relationships (remove relação WORKS_AT)

Como rodar (local):

1. Instale dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Ajuste variáveis de ambiente se necessário (ex.: `APP_NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`).

3. Rode a API:

```bash
uvicorn main:api --reload --host 0.0.0.0 --port 8000
```

Obs: Este projeto supõe que um servidor Neo4j esteja disponível e acessível na URI configurada.

