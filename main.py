from flask import Flask, jsonify, request
import json
from flask import jsonify
from flask_socketio import SocketIO
import os
from flask_migrate import Migrate
from seed import *
from models.equipment import *
from models.material import *
from models.alert import *
from responses.material import *
from responses.alert import *
import datetime
from sqlalchemy.orm import aliased
from dateutil import parser
from flask_mqtt import Mqtt
from app import setup_flask_app
from models.main import *

app = setup_flask_app()
BROKER_TOPIC_MATERIAL = 'MATERIALS'
BROKER_TOPIC_EQUIPMENT = 'HUDDLE_EQUIPAMENTOS'

mqtt = Mqtt(app)
socketio = SocketIO(app)
print("==============================")
print(app.config['sqlalchemy.url'])
print(app.config['MQTT_BROKER_URL'])
db.init_app(app)
migrate = Migrate() 
migrate.init_app(app, db)

result_material = []
result_equipment = []

app = setup_flask_app()
BROKER_TOPIC = 'HUDDLE_MATERIAIS'


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
            query_material = MaterialMeasurement.query.filter(MaterialMeasurement.id >= q.beginmeasure.id).filter(MaterialMeasurement.id <= q.endmeasure.id).all()
            min_temperature = float(os.getenv('MIN_TEMPERATURE'))
            max_temperature = float(os.getenv('MAX_TEMPERATURE'))
            min_humidity = float(os.getenv('MIN_HUMIDITY'))
            max_humidity = float(os.getenv('MAX_HUMIDITY'))
            temps_bool = [ m.temperature > max_temperature or m.temperature < min_temperature for m in query_material]
            hum_bool = [ m.humidity > max_humidity or m.humidity < min_humidity for m in query_material]
            if(all(hum_bool)):
                q.humidities = query_material
            else:
                q.humidities = []
            if(all(temps_bool)):
                q.temperatures = query_material
            else:
                q.temperatures = []
        obj = {"materials":query}
        schema = Alert(many=True)
        result = schema.dumps(obj)
        return result

@app.route("/iot/materials")
def materials():
    args = request.args
    if("numberOfItems" in args):
        query_materials = MaterialMeasurement.query.order_by(MaterialMeasurement.timeOfMeasurements).limit(args["numberOfItems"])
    else:
        query_materials = MaterialMeasurement.query.order_by(MaterialMeasurement.timeOfMeasurements).all()
    
    schema = MaterialSchema(many=True)
    result = schema.dumps(query_materials)
    return result


@app.route("/iot/equipments")
def equipments():
    print(EquipmentMeasurement.query.first().__dict__)

    return jsonify(EquipmentMeasurement.query.all())


def handle_mqtt_material(obj):
    print("--------------------")
    with app.app_context():
        device = Device.query.filter(Device.mac == obj["MACADDRESS"]).first()
        if(device is None):
            device = Device(mac=obj["MACADDRESS"])
            db.session.add(device)
            db.session.commit()
        sensor = SensorsMaterial.query.join(Device).filter(SensorsMaterial.id == int(obj["idSensor"])).filter(Device.mac == obj["MACADDRESS"]).first()
        if(sensor is None):
            sensor = SensorsMaterial(id=int(obj["idSensor"]), device_id=device.id)
            db.session.add(sensor)
            db.session.commit()
        timeOfMeasurements = parser.parse(obj['timeOfMessage'])
        material = MaterialMeasurement(temperature=obj['temperature'], humidity=obj['humidity'],
        timeOfMeasurements=timeOfMeasurements,sensor_id =sensor.id)
        db.session.add(material)
        db.session.commit()
        time_elapsed = int(os.getenv('MIN_ELAPSED_TIME_IN_SECONDS'))
        last_relevant_measure = material.timeOfMeasurements - datetime.timedelta(seconds=time_elapsed)
        min_temperature = float(os.getenv('MIN_TEMPERATURE'))
        max_temperature = float(os.getenv('MAX_TEMPERATURE'))
        min_humidity = float(os.getenv('MIN_HUMIDITY'))
        max_humidity = float(os.getenv('MAX_HUMIDITY'))
        query_material = MaterialMeasurement.query.filter(MaterialMeasurement.timeOfMeasurements > last_relevant_measure).all() 
        last = query_material[-1]
        temps_bool = [ m.temperature > max_temperature or m.temperature < min_temperature for m in query_material]
        hum_bool = [ m.humidity > max_humidity or m.humidity < min_humidity for m in query_material]
        if(all(temps_bool) or all(hum_bool)):
            current_alert = AlertMaterial.query.first()
            BeginMeasure = aliased(MaterialMeasurement)
            EndMeasure = aliased(MaterialMeasurement)
            current_alert = AlertMaterial.query.join(BeginMeasure,'beginmeasure').join(EndMeasure,'endmeasure').filter(BeginMeasure.timeOfMeasurements < last.timeOfMeasurements).filter(EndMeasure.timeOfMeasurements > last.timeOfMeasurements).first()
            if current_alert == None:
                alert = Alert()
                db.session.add(alert)
                db.session.commit()
                alert_m = AlertMaterial(begin_meassurement_id = last.id , end_meassurement_id = material.id, alert_id= alert.id)
                db.session.add(alert_m)
                db.session.commit()
            else:
                print("Second")
                current_alert.end_measure = material.id
                db.session.commit()


@mqtt.on_message()
def handle_mqtt(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode())
    )
    result_material.append(data['payload'])
    obj = data['payload']
    if data["topic"] == "MATERIALS":
        handle_mqtt_material(obj)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mqtt.subscribe(BROKER_TOPIC_MATERIAL)
    mqtt.subscribe(BROKER_TOPIC_EQUIPMENT)
    print(mqtt.topics)
    app.run(host="0.0.0.0", port=5000, debug=True)
