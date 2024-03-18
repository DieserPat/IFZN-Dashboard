# -*- coding: utf-8 -*-
from .createSocket import TCPSocket
from .processMessage import processReply, log

def connectThrottle(ip, port, mode):
    if mode == "0" or mode == 0:
        key = "start"
    else:
        key = "stop"
    enable, sock = TCPSocket(ip=ip, port=port)
    active = 0
    if enable:
        try:
            sock.sendall("\x02 {} \x03\n".format(key).encode())
            reply = sock.recv(1024)
            active = 1
            success, _ = processReply(reply, key, "Thortle")
            if success:
                active = 1
        except:
            active = 0
            log("Thortle", "Error in connecting to the server", "error")
        sock.close()
    return active


def setThrottle(setpoint, ip, port, keyword):
    enable, sock = TCPSocket(ip=ip, port=port)
    succes, value = False, 0
    if enable:
        try:
            sock.sendall("\x02 s{} \x03\n".format(setpoint).encode())
            reply = sock.recv(1024)
            success, value = processReply(reply, keyword, "Thortle", True, valChar=keyword)
        except:
            log("Thortle", "Error in connecting to the server", "error")
        sock.close()
    return value

def getThrottle(ip, port, keyword, v0=0.89, v100=4.32):
    enable, sock = TCPSocket(ip=ip, port=port)
    succes, value = False, 0
    if enable:
        try:
            sock.sendall("\x02 meas \x03\n".encode())
            reply = sock.recv(1024)
            success, value = processReply(reply, keyword, "Thortle", True, valChar=keyword)
            position = (float(value) - v0) / (v100-v0) * 100
        except:
            log("Thortle", "Error in connecting to the server", "error")
        sock.close()
    return position


# ETH-connection data for the throttle arduino: ip, port = "192.168.1.20", 3003
# ip, port = "192.168.1.20", 3003



    