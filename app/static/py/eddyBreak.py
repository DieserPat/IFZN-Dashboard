# -*- coding: utf-8 -*-
import serial
from pandas import read_csv

def connectSerial(port, baudrate=115200):
    try:
        ser = serial.Serial(
            # used port from the function input
            port=port.upper(),
            # the baudrate of the sender and receiver must be the same, ...
            baudrate=baudrate,
            # ... as well as the pairty ...
            parity=serial.PARITY_NONE,
            # ... the stopbits ...
            stopbits=serial.STOPBITS_ONE,
            # ... and the bytesize. The settings are written at the top!
            bytesize=serial.EIGHTBITS,
            timeout= 1)
        return ser, True
    except:
        return None, False


def connectBreak(port):
    serialConnector, flag = connectSerial(port)
    if flag:
        serialConnector.close()
    return flag


def readError(error):
    errorList = []
    errNum = bin(error)[2:] if len(bin(error)) > 8 else bin(error)
    errorCodesPath = r"app/static/notes/error_eddy_break.txt"
    errorCodes = read_csv(errorCodesPath, sep=",", index_col="bin")
    for i in range(len(errNum)):
        if errNum[i] == "1":
            errorList.append(errorCodes.loc[7-i]["message"])
    return errorList


def readDat(port):
    serialConnector, flag = connectSerial(port)
    dat = dict()
    flagDat = False
    dat["flag"] = 0
    if flag:
        try:
            datProt = serialConnector.read_until(b"\r\n").decode()
            if datProt == "":
                flagDat = False
            else:
                dat["nEng"] = datProt[3:7]
                dat["nEngSetpoint"] = datProt[7:11]
                dat["mEng"] = datProt[11:14]
                dat["TBreak"] = datProt[14:17]
                dat["Error"] = int(datProt[17:20])
                dat["flag"] = 1
                if dat["Error"] != 0:
                    dat["ErrorList"] = readError(dat["Error"])
                flagDat = True
        except:
            pass
        serialConnector.close()
    return flagDat, dat

def sendSet(port, setpoint):
    serialConnector, flag = connectSerial(port)
    flagSend = False
    if flag:
        try:
            serialConnector.write(("set%04d" % setpoint).encode())
            flagSend = True
        except:
            pass
        serialConnector.close()
    return flagSend

"""
from app.static.py.eddyBreak import connectBreak, readDat, sendSet

com, value = "com6", 2500
value=2500
connectBreak(com)
sendSet(com, value)
readDat(com)

ser, flag = connectSerial(port, baud)
port, baud = "com6", 115200
readDat(ser)

"""