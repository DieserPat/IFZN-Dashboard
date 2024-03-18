# # -*- coding: utf-8 -*-
# """
# Created on Mon Jan 16 12:43:25 2023

# @author: gross
# """

# # import socket

# # ip, port = "192.168.1.72", 5005

# # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # sock.bind(("", port))
# # sock.settimeout(1)

# # def send():
# #     sock.sendto(b"x02/OK/x03", (ip, port))
# #     data, addr = sock.recvfrom(1024)
# #     print(data, addr)
# import logging
# from datetime import datetime

# def log(modul, message, logType):
#     logging.basicConfig(filename='../logging/connections.log', filemode='w', level=logging.INFO)
#     dateTime = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
#     logMsg = "{}-{}: {}".format(dateTime, modul, message)
#     if logType == "error":
#         logging.error(logMsg)
#     elif logType == "warning":
#         logging.warning(logMsg)
#     else:
#         logging.info(logMsg)
            
    

# flag = False
# value = None
# expectedVal = ["p", "m"]
# msg = "start"
# val = ""
# ans = "\x02 OK {}{} \x04".format(msg, val)
# ans_split = ans.split(" ")
# if ans_split[0] == "\x02" and ans_split[-1] == "\x03":
#     if ans_split[1] == "OK":
#         if ans_split[2] == msg:
#             flag = True
#             if msg[0] in expectedVal:
#                 if ans_split[3][0] == "v":
#                     value = ans_split[3][1]
#                 else:
#                     log("Relais", "The replied message has no value", "warning")
#         else:
#             log("Relais", "The replied message does not corresponds to the send message", "error")
#     else:
#         log("Relais", "The replied message is not OK", "error")
# else:
#     log("Relais", "The replied message contains no start or stop bit!", "error")

# print(flag, value)

import logging
from datetime import datetime

def log(modul, message, logType):
    logging.basicConfig(filename='../Dashboard/app/static/logging/connections.log', filemode='w', level=logging.INFO)
    dateTime = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    logMsg = "{}-{}: {}".format(dateTime, modul, message)
    if logType == "error":
        logging.error(logMsg)
    elif logType == "warning":
        logging.warning(logMsg)
    else:
        logging.info(logMsg)


def processReply(replyMessage, keyword, modul, expectVal=False, sep=" ", stx="\x02", etx="\x03", valChar="v"):
    flag = False
    value = None
    replyFrac = replyMessage.split(sep)
    print(replyFrac)
    if replyFrac[0] == stx and replyFrac[-1] == etx:
        if replyFrac[1] == "OK":
            if replyFrac[2] == keyword:
                flag = True
                if expectVal:
                    if replyFrac[3][0] == valChar:
                        value = replyFrac[3][1]
                    else:
                        log(modul, "The replied message has no value", "warning")
            else:
                log(modul, "The replied message does not corresponds to the send message", "error")
        else:
            log(modul, "The replied message is not OK", "error")
    else:
        log(modul, "The replied message contains no start or stop bit!", "error")

    return(flag, value)

