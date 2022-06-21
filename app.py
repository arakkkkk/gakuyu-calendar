from flask import Flask, Blueprint, session, redirect, url_for, abort, request
from flask_cors import CORS
from flask import render_template
import json
import glob
from src import util
from api.calendarApi import CalendarApi
app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/equipments')
def equipments_index():
    return render_template("equipments/index.html")

@app.route('/equipments/insert')
def equipments_insert():
    equip_json = util.getJsonByDirectory("data/equipments")
    return render_template("equipments/insert.html", equip_json=equip_json)

@app.route('/equipments/list')
def equipments_list():
    api = CalendarApi()
    return render_template("equipments/list.html")


@app.route('/api/equipments/list', methods=["POST"])
def api_equipments_list():
    api = CalendarApi()
    reservations = api.get(
            start = util.request2datetime(request.json["start"]).isoformat(),
            end = util.request2datetime(request.json["end"]).isoformat()
            )
    return json.dumps(reservations)

@app.route('/api/equipments/insert', methods=["POST"])
def api_equipments_insert():
    json = request.json
    api = CalendarApi()
    api.insert(
            title = json["title"],
            description_json = json["description"],
            start = util.request2datetime(json["start"]).isoformat(),
            end = util.request2datetime(json["end"]).isoformat()
            )
    return json

@app.route('/api/equipments/delete', methods=["POST"])
def api_equipments_delete():
    api = CalendarApi()
    res = api.delete(
            event_id = request.json["event_id"]
            )
    return json.dumps(res)

@app.route('/api/equipments/update', methods=["POST"])
def api_equipments_update():
    api = CalendarApi()
    status = request.json["status"]
    event_id = request.json["event_id"]
    if status == "予約":
        res = api.update(event_id, status="予約")
    elif status == "貸出":
        res = api.update(event_id, status="貸出")
    elif status == "返却":
        res = api.update(event_id, status="返却")
    return json.dumps(res)

app.run(port=8081, debug=True)
