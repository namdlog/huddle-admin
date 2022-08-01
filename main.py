from flask import request, jsonify
from models.equipment import *
from models.material import *
from models.alert import *
from models.task import *
from models.user import *
from responses.alert import *
from responses.task import *
from responses.user import *
from app import setup_flask_app
from broker import setup_mqtt_broker, result_material, MAX_HUMIDITY, MIN_HUMIDITY, MAX_TEMPERATURE, MIN_TEMPERATURE

app = setup_flask_app()
mqtt = setup_mqtt_broker(app)


@app.route("/")
def hello_world():
    return {"data": result_material}


@app.route("/alerts")
def alerts():
    query = AlertMaterial.query.all()
    if query is None:
        return []
    else:
        for q in query:
            query_material = MaterialMeasurement.query.filter(MaterialMeasurement.id >= q.beginmeasure.id)\
                .filter(MaterialMeasurement.id <= q.endmeasure.id).all()
            min_temperature = MIN_TEMPERATURE
            max_temperature = MAX_TEMPERATURE
            min_humidity = MIN_HUMIDITY
            max_humidity = MAX_HUMIDITY
            temps_bool = [ m.temperature > max_temperature or m.temperature < min_temperature for m in query_material]
            hum_bool = [ m.humidity > max_humidity or m.humidity < min_humidity for m in query_material]
            if all(hum_bool):
                q.humidities = query_material
            else:
                q.humidities = []
            if all(temps_bool):
                q.temperatures = query_material
            else:
                q.temperatures = []
        obj = {"materials": query}
        schema = Alert(many=True)
        result = schema.dumps(obj)
        return result


@app.route("/iot/materials")
def materials():
    args = request.args
    if "numberOfItems" in args:
        query_materials = MaterialMeasurement.query\
            .order_by(MaterialMeasurement.timeOfMeasurements).limit(args["numberOfItems"])
    else:
        query_materials = MaterialMeasurement.query.order_by(MaterialMeasurement.timeOfMeasurements).all()

    schema = MaterialSchema(many=True)
    result = schema.dumps(query_materials)
    return result


@app.route("/iot/equipments")
def equipments():
    print(EquipmentMeasurement.query.first().__dict__)

    return jsonify(EquipmentMeasurement.query.all())

@app.route("/task", methods=['POST'])
def create_task():
  created_at = datetime.now()
  responsable_id = request.json['responsable_id']
  status = request.json['status']
  date_to_complete = datetime.strptime(request.json['date_to_complete'], '%d/%m/%Y %H:%M:%S')
  alert_id = request.json['alert_id']
  task = Task(created_at=created_at, responsable_id=responsable_id, status=status, date_to_complete=date_to_complete, alert_id=alert_id)
  db.session.add(task)
  db.session.commit()


@app.route("/tasks", methods=['GET'])
def tasks():
    query_tasks = Task.query.all()
    
    schema = TaskSchema(many=True)
    result = schema.dumps(query_tasks)
    return result

@app.route("/task", methods=['GET'])
def task():
    args = request.args
    if "taskId" in args:
        query_task = Task.query\
                         .filter(Task.id == args["taskId"]).all()
    else:
      query_task = Task.query.all()

    schema = TaskSchema(many=True)
    result = schema.dumps(query_task)
    return result

@app.route("/task", methods=['DELETE'])
def delete_task():
    task_id = request.json['id']
    if task_id >= 0:
        Task.query.filter(Task.id == task_id).delete()
    else:
      return {}

    db.session.commit()
    return {}

@app.route("/task", methods=['PUT'])
def update_task():
    task_id = request.json['id']
    responsable_id = request.json['responsableId']
    status = request.json['status']
    date_to_complete = request.json['dateToComplete']
    alert_id = request.json['alertId']

    if task_id >= 0:
        task = Task.query.get(task_id)
        task.responsable_id = responsable_id
        task.status = status
        task.date_to_complete = date_to_complete
        task.alert_id = alert_id
    else:
      return {}

    db.session.commit()
    return {}

@app.route("/auth/cadastro", methods=['POST'])
def create_user():
  name = request.json['name']
  email = request.json['email']
  password = request.json['password']
  isAdmin = request.json['isAdmin']
  rfid = request.json['rfid']
  card_type = request.json['card_type']
  sector = request.json['sector']
  extension_number = request.json['extension_number'] 
  user = User (name = name, email = email, password = password, isAdmin = isAdmin, rfid = rfid, card_type = card_type, sector = sector, extension_number = extension_number)
  db.session.add(user)
  db.session.commit()

@app.route("/auth/login", methods=['GET'])
def login():
    query_user = User.query\
                         .filter(User.email == request.args["email"]).first()

    schema = UserSchema(many=True)
    result = schema.dumps(query_user)

    if result is not None and result['password'] == request.args['password']:
            return result

    return 'User/password invalid'

@app.route("/users", methods=['GET'])
def users():
    query_users = User.query.all()
    
    schema = UserSchema(many=True)
    result = schema.dumps(query_users)
    return result

@app.route("/user", methods=['GET'])
def user():
    args = request.args
    if "email" in args:
        query_user = User.query\
                         .filter(User.email == args["email"]).all()
    else:
      query_user = User.query.all()

    schema = UserSchema(many=True)
    result = schema.dumps(query_user)
    return result

@app.route("/user", methods=['DELETE'])
def delete_user():
    user_id = request.json['id']
    if user_id >= 0:
        User.query.filter(Task.id == user_id).delete()
    else:
      return {}

    db.session.commit()
    return {}

@app.route("/user", methods=['PUT'])
def update_user():
    id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    isAdmin = request.json['isAdmin']
    rfid = request.json['rfid']
    card_type = request.json['card_type']
    sector = request.json['sector']
    extension_number = request.json['extension_number']

    if id >= 0:
        user = User.query.get(id)
        user.name = name
        user.email = email
        user.password = password
        user.isAdmin = isAdmin
        user.rfid = rfid
        user.card_type = card_type
        user.sector = sector
        user.extension_number = extension_number
    else:
      return {}

    db.session.commit()
    return {}



if __name__ == '__main__':
    print(mqtt.topics)
    app.run(host="0.0.0.0", port=5000, debug=True)
