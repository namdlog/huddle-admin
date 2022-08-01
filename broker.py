import json, os
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from sqlalchemy.orm import aliased

from models.material import *
from models.alert import Alert, AlertMaterial

BROKER_TOPIC_MATERIAL = 'MATERIALS'
BROKER_TOPIC_EQUIPMENT = 'HUDDLE_EQUIPAMENTOS'
result_material = []
result_equipment = []


def handle_mqtt_material(app, obj):
    print("--------------------")
    with app.app_context():
        device = Device.query.filter(Device.mac == obj["MACADDRESS"]).first()
        if device is None:
            device = Device(mac=obj["MACADDRESS"])
            db.session.add(device)
            db.session.commit()
        sensor = SensorsMaterial.query.join(Device).filter(SensorsMaterial.id == int(obj["idSensor"])).filter(Device.mac == obj["MACADDRESS"]).first()
        if sensor is None:
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


def setup_mqtt_broker(app):
    mqtt = Mqtt(app)
    socketio = SocketIO(app)

    @mqtt.on_message()
    def handle_mqtt(client, userdata, message):
        data = dict(
            topic=message.topic,
            payload=json.loads(message.payload.decode())
        )
        result_material.append(data['payload'])
        obj = data['payload']
        if data["topic"] == "MATERIALS":
            handle_mqtt_material(app, obj)

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)

    mqtt.subscribe(BROKER_TOPIC_MATERIAL)
    mqtt.subscribe(BROKER_TOPIC_EQUIPMENT)
    return mqtt
