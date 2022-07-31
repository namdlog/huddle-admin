# Como rodar localmente

## Docker
### Definir variavéis de ambiente no arquivo `.env` na raiz do projeto como está no .env.example
```sh
BROKER_URL=;
BROKER_PORT=;
BROKER_USERNAME=;
BROKER_PASSWORD=;
DB_URL=postgresql://postgres:postgres@db:5432/postgres
```

## Migras as models 
docker-compose up db 
### Em outra aba 
docker-compose run flask sh 
export FLASK_APP= main
flask db migrate 
flask db upgrade


### Inicializar com docker-compose
```sh
docker-compose up -d 
```

API disponível em localhost:5000

### Acessar DB
```sh
docker exec -it huddle-admin_db_1 psql -U postgres
```