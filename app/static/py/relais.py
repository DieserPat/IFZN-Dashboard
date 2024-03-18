# -*- coding: utf-8 -*-
from .createSocket import TCPSocket
from .processMessage import processReply, log

def connectRelais(ip, port, mode, num_of_relais=6):
    if mode == "0":
        key = "start"
    else:
        key = "stop"
    enable, relais_socket = TCPSocket(ip=ip, port=port)
    active = 0
    relaisState = dict()
    if enable:
        try:
            relais_socket.sendall("\x02 {} \x03\n".format(key).encode())
            reply = relais_socket.recv(1024)
            relais_socket.close()
            active = 1
            success, _ = processReply(reply, key, "Relais")
            if success:
                for i in range(num_of_relais):
                    if key == "start":
                        value = setRelais(relais_number=i, relais_state=0, ip=ip, port=port)
                    else:
                        value = getRelais(relais_number=i, ip=ip, port=port)
                    relaisState[i] = value
                active = 1
        except:
            active = 0
            log("Relais", "Error in connecting to the server", "error")
            relais_socket.close()
    return active, relaisState
    
def setRelais(relais_number, relais_state, ip, port):
    enable, relais_socket = TCPSocket(ip=ip, port=port)
    succes, value = False, 0
    if enable:
        try:
            relais_socket.sendall("\x02 p{} v{} \x03\n".format(relais_number, relais_state).encode())
            reply = relais_socket.recv(1024)
            success, value = processReply(reply, "p", "Relais", True)
        except:
            log("Relais", "Error in connecting to the server", "error")
        relais_socket.close()
    return value

def getRelais(relais_number, ip, port):
    enable, relais_socket = TCPSocket(ip=ip, port=port)
    succes, value = False, 0
    if enable:
        try:
            relais_socket.sendall("\x02 m{} \x03\n".format(relais_number).encode())
            reply = relais_socket.recv(1024)
            success, value = processReply(reply, "m", "Relais", True)
        except:
            log("Relais", "Error in connecting to the server", "error")
        relais_socket.close()
    return value

# ETH-connection data for the relais-PCB: ip, port = "192.168.1.72", 5005
# ip, port = "192.168.1.72", 5005



    