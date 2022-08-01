from flask import request, jsonify
import os
from models.equipment import *
from models.material import *
from models.alert import *
from responses.alert import *
from app import setup_flask_app
from broker import setup_mqtt_broker, result_material

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
    if "numberOfItems" in args:
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


if __name__ == '__main__':
    print(mqtt.topics)
    app.run(host="0.0.0.0", port=5000, debug=True)
