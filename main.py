from flask import Flask,jsonify
import json
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import os
from flask_mqtt import Mqtt
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from models.models import *

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.getenv('BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('BROKER_PORT'))
app.config['MQTT_USERNAME'] = os.getenv('BROKER_USERNAME')
app.config['MQTT_PASSWORD'] = os.getenv('BROKER_PASSWORD')
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['sqlalchemy.url'] = os.getenv('DB_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BROKER_TOPIC = 'HUDDLE_MATERIAIS'

mqtt = Mqtt(app)
socketio = SocketIO(app)
print("==============================")
print(app.config['sqlalchemy.url'])
print(app.config['MQTT_BROKER_URL'])
db.init_app(app)
migrate = Migrate() 
migrate.init_app(app, db)
result = []
with app.app_context():
  from flask_migrate import upgrade as _upgrade
  from flask_migrate import migrate as _migrate
  _migrate()
  _upgrade()

@app.route("/")
def hello_world():
    return {"data": result}


@app.route("/iot/materials")
def materials():
    print(MaterialMeasurement.query.first().__dict__)
    return jsonify(MaterialMeasurement.query.all())

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode())
    )
    print(data)
    result.append(data['payload'])
    obj = data['payload']
    print(obj['temperatura'])
    with app.app_context():
        material = MaterialMeasurement(temperature=obj['temperatura'],humidity=obj['umidade'],
        timeOfMeasurements=obj['dataHoraMedicao'])
        print(material.__dict__)
        db.session.add(material)
        db.session.commit()
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mqtt.subscribe(BROKER_TOPIC)
    print(mqtt.topics)
    app.run(host="0.0.0.0", port=5000,debug=True)