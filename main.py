from flask import Flask,jsonify
import json
from flask import jsonify
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from app import setup_flask_app

from models.equipment import *
from models.material import *

app = setup_flask_app()
BROKER_TOPIC_MATERIAL = 'HUDDLE_MATERIAIS'
BROKER_TOPIC_EQUIPMENT = 'HUDDLE_EQUIPAMENTOS'

mqtt = Mqtt(app)
socketio = SocketIO(app)
result_material = []
result_equipment = []

@app.route("/")
def hello_world():
    return {"data": result_material}


@app.route("/iot/materials")
def materials():
    print(MaterialMeasurement.query.first().__dict__)
    return jsonify(MaterialMeasurement.query.all())


@mqtt.on_message()
def handle_mqtt_material(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode())
    )
    print(data)
    result_material.append(data['payload'])
    obj = data['payload']
    print(obj['temperatura'])
    with app.app_context():
        material = MaterialMeasurement(temperature=obj['temperatura'], humidity=obj['umidade'],
                                       timeOfMeasurements=obj['dataHoraMedicao'])
        print(material.__dict__)
        db.session.add(material)
        db.session.commit()
    socketio.emit('mqtt_message', data=data)


@mqtt.on_message()
def handle_mqtt_equipment(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode())
    )
    print(data)
    result_equipment.append(data['payload'])
    obj = data['payload']
    print(obj)
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mqtt.subscribe(BROKER_TOPIC_MATERIAL)
    mqtt.subscribe(BROKER_TOPIC_EQUIPMENT)
    print(mqtt.topics)
    app.run(host="0.0.0.0", port=5000, debug=True)
