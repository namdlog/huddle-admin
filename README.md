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
flask db init
cd migrations
mkdir versions
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

### Inserir uma task
task = {'responsable_id':3,'status':'testee','date_to_complete':'10/10/2022 10:10:10','alert_id':9}
fetch('/task/new', {
  method: 'POST',
  body: JSON.stringify(task),
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)

### Consultar uma task
/task?taskId=[ID_DA_TASK]

### Update task
novaTask = {'id':1, 'status':'novo status','responsableId':4,'alertId':10,'dateToComplete': '2022-10-11T11:11:11'}
fetch('/task', {
  method: 'PUT',
  body: JSON.stringify(novaTask),
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)

### Deletar task
delecao = {'id':2}
fetch('/task', {
  method: 'DELETE',
  body: JSON.stringify(delecao),
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)

### Consultar todas as tasks
/tasks