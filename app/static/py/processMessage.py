import logging
from datetime import datetime

def log(modul, message, logType):
    logging.basicConfig(filename='../GH_Dash/app/static/logging/connections.log', filemode='w', level=logging.INFO)
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
    replyFrac = replyMessage.decode().replace("\n", "").split(sep)
    if replyFrac[0] == stx and replyFrac[-1] == etx:
        if replyFrac[1] == "OK":
            if len(replyFrac[2]) > len(keyword):
                compare = replyFrac[2][0]
            else:
                compare = replyFrac[2]
            if compare == keyword:
                flag = True
                if expectVal:
                    index = len(replyFrac) - 2
                    if replyFrac[index][0] == valChar:
                        value = replyFrac[index][1:]
                    else:
                        log(modul, "The replied message has no value", "warning")
            elif len(replyFrac) == 4:
                flag = True
                value = float(replyFrac[2])
            else:
                log(modul, "The replied message does not corresponds to the send message", "error")
        else:
            log(modul, "The replied message is not OK", "error")
    else:
        log(modul, "The replied message contains no start or stop bit!", "error")

    return(flag, value)