# Laboratório: FastAPI + MySQL (RDS) no AWS App Runner

Aplicação simples em FastAPI para testar o fluxo **GitHub → App Runner** conectando-se a um **MySQL no RDS** via SQLAlchemy.

## Requisitos
- Python 3.10+
- Banco MySQL acessível (RDS recomendado)

Variáveis de ambiente esperadas:
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

## Executar localmente
```bash
python -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt

export DB_HOST=...
export DB_PORT=3306
export DB_NAME=apprunner
export DB_USER=admin
export DB_PASSWORD=xxxx

uvicorn app.main:app --host 0.0.0.0 --port 8080
```
Abra em `http://localhost:8080` e crie/anote dados para validar escrita/leitura no MySQL.

## Estrutura rápida
- `app/main.py`: rotas FastAPI e integração SQLAlchemy
- `app/db.py` e `app/config.py`: criação do engine e leitura de envs
- `app/models.py`: modelo `Note`
- `templates/index.html`: tela HTML simples para testar CRUD
- `apprunner.yaml`: instruções de build/run para o App Runner

## Deploy no AWS App Runner (fonte GitHub)
1) Suba este repositório no GitHub.  
2) No console do App Runner, crie um serviço com fonte **Repositorio → GitHub** apontando para este repo/branch.  
3) Garanta que o arquivo `apprunner.yaml` está na raiz.  
4) Configure variáveis de ambiente/segredos:
   - Use os campos de env ou o **Secrets Manager** (recomendado) para `DB_PASSWORD`.
5) Selecione porta de escuta `8080` (bate com o `run.network.port`).  
6) Finalize a criação; o App Runner cuidará do build (`pip install -r requirements.txt`) e iniciará `uvicorn app.main:app --host 0.0.0.0 --port 8080`.

### Rede e segurança
- O serviço precisa conseguir alcançar o endpoint do RDS.  
  - Preferencial: crie o App Runner **conectado a um VPC Connector** com rotas privadas para o RDS.  
  - Alternativa para laboratório: abra o RDS via Security Group/ACL para o IP de saída do App Runner (não recomendado para produção).

### Testes pós-deploy
- Acesse a URL pública do App Runner → salve uma anotação → confirme leitura.  
- API também disponível em `GET /api/notes` e `POST /api/notes` (JSON).

## Customizações sugeridas
- Mover a senha para Secrets Manager (já previsto em `apprunner.yaml` via `envSecrets`).  
- Adicionar migrações com Alembic caso o schema evolua.  
- Trocar MySQL por Aurora Serverless v2 para reduzir custos em laboratório.


