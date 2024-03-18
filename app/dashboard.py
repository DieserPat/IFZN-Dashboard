from app import app
from flask import render_template, request, jsonify, make_response
from app.static.py.constData import fetchConstData, fetchData
from time import sleep
from .static.py.relais import connectRelais, setRelais
from .static.py.throttle import connectThrottle, setThrottle, getThrottle
from .static.py.PLU4000 import setMessage, initialize, start, stop, statMeasurment
from .static.py.eddyBreak import connectBreak, sendSet, readDat
import psutil

import inspect


def printValues(PLU):
    print("******* New Data *******")
    for i in inspect.getmembers(PLU):
        if not i[0].startswith("_") and i[0].startswith("respond"):
            if not inspect.ismethod(i[1]):
                print(i)


constDataPath = r"app/static/data/extDash.xlsx"
dataPath = r"app/static/data/data.csv"

constData = fetchConstData(constDataPath)
PLU = setMessage()
shut_off_errors = [3, 4, 5, 6, 7, 8, 9]

app.debug = True

@app.route("/Dashboard")
def dash():
    return render_template("dashboard.html", content=constData)

@app.route("/Dashboard/Relais", methods=["POST"])
def relais():
    req = request.get_json()
    if req.get('mode') == 'setRelais':
        id = req.get("id")[-1]
        setState = int(not(int(req.get("value"))))
        state = setRelais(relais_number=id, relais_state=setState, ip=req.get("ip"), port=int(req.get("port")))
        if state is not None:
            req["value"] = state
        res = make_response(jsonify(req), 200)
        # sleep(1)
    elif req.get('mode') == 'activateRelais':
        enable, RelaisState = connectRelais(ip=req.get("ip"), port=int(req.get("port")), mode=req.get("value"))
        if enable:
            req["value"] = not(bool(int(req.get("value"))))
        res = make_response(jsonify(req), 200)
    return res

@app.route("/fetchData", methods=["GET"])
def returnData():
    data = fetchData(dataPath)
    res = make_response(jsonify(data), 200)
    # print(data)
    return res

@app.route("/Dashboard/fetch/Break", methods=["POST"])
def fetchBreak():
    req = request.get_json()
    com = req.get("com")
    flag, dat = readDat(com)
    return make_response(jsonify(dat), 200)

@app.route("/Dashboard/fetch/Throttle", methods=["POST"])
def fetchThrottle():
    req = request.get_json()
    ip = req.get("ip")
    port = int(req.get("port"))
    value = getThrottle(ip, port, "m")
    # print(value)
    data = {
        "throttlePos": float(value)
    }
    res = make_response(jsonify(data), 200)
    return res

@app.route("/Dashboard/fetch/PLU", methods=["POST"])
def fetchPLU():
    req = request.get_json()
    com = req.get("com")
    measruementMode = req.get("mode")
    # printValues(PLU)
    if measruementMode == "stat":
        statMeasurment(com, PLU, shut_off_errors)
        # Generaldata = fetchData(dataPath)
        data = {
            # "respond_mean_value": Generaldata["PLUstat"],
            # "respond_temperature": Generaldata["PLUTemp"],
            "respond_mean_value": PLU.respond_mean_value,
            "respond_temperature": PLU.respond_temperature
        }
        res = make_response(jsonify(data), 200)
    else:
        res = make_response(jsonify(req), 200)
    return res

@app.route("/Dashboard/Throttle", methods=["POST"])
def throttle():
    req = request.get_json()
    ip = req.get("ip")
    port = int(req.get("port"))
    value = int(req.get("value"))
    if req.get("mode") == "set":
        # set position in script
        setValue = setThrottle(value, ip, port, "s")
        req["value"] = setValue
        # req["value"] = int(req.get("value"))
        res = make_response(jsonify(req), 200)
    elif req.get('mode') == 'activate':
        # function to activate or deactivate the arduino
        active = connectThrottle(ip=ip, port=port, mode=value)
        if active:
            req["value"] = not(bool(int(req.get("value"))))
        # if int(req["value"]) == 0:
        #     req["value"] = 1
        # else:
        #     req["value"] = 0
        res = make_response(jsonify(req), 200)

    return res

@app.route("/Dashboard/Break", methods=["POST"])
def eddyBreak():
    req = request.get_json()
    value = int(req.get("value"))
    com = req.get("com")
    
    if req.get("mode") == "set":
        setBreak = sendSet(com, value)
        req["flag"] = False
        if setBreak:
            flag, dat = readDat(com)
            if flag and int(dat["nEngSetpoint"]) == int(value):
                req["flag"] = setBreak
        res = make_response(jsonify(req), 200) 
    elif req.get('mode') == 'activate':
        available = connectBreak(com)
        req["value"] = int(available)
        res = make_response(jsonify(req), 200)

    return res

@app.route("/Dashboard/PLU", methods=["POST"])
def setPLU():
    req = request.get_json()
    com = req.get("com")
    res = make_response(jsonify(req), 200)
    # print(req)
    if req.get("mode") == "start":
        startPump = start(com, PLU, shut_off_errors)
        # startPump = 1
        req["value"] = int(startPump)
        res = make_response(jsonify(req), 200)
        # sleep(1)
    elif req.get("mode") == "stop":
        i = 0
        while i < 25:
            stopPump = stop(com, PLU)
            if int(stopPump) == 1:
                break
            sleep(0.1)
            i += 1
        # stopPump = 1
        req["value"] = int(stopPump)
        res = make_response(jsonify(req), 200)
        # sleep(1)
    elif req.get('mode') == 'activate':
        if int(req["value"]) == 0:
            init = initialize(com, PLU)
            # init = True
            req["value"] = int(init)
        res = make_response(jsonify(req), 200)
    # print(req)
    return res

@app.route("/Dashboard/CPU", methods=["POST"])
def getCPURAM():
    res = {
        "cpu": psutil.cpu_percent(1),
        "ram": psutil.virtual_memory()[2]
    }
    return make_response(jsonify(res), 200)
