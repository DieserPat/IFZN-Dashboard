# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:26:37 2021

@author: gross
"""


class Message:
    """class to sort the send and received message"""

    def __init__(self, message, mode, no_rx=False):
        if not no_rx:
            try:
                # delete the start-bit ...
                msg = message.replace("\x02 ", "")
                # ... and the stop-bit from the messages
                msg = msg.replace(" \x03", "")
            except:
                msg = message
            self.message = msg
            # ... and split the messages by space
            msg = msg.split(" ")
    
            if mode == "rx":
                # sort the received message by function code, error-status, error-code, task and data
                self.function_code = msg[0]
                self.error_status = int(msg[1])
                self.error_code = msg[3]
                self.task = int(msg[4])
                self.error = None
                self.checksum = None
                self.AZ = None
                self.respond = None
                self.abort = False
                if len(msg) > 4:
                    self.data = list(float(data) for data in msg[5:])
                else:
                    self.data = None
            elif mode == "tx":
                # sort the sent message by function code, task and data
                self.function_code = msg[0]
                self.task = int(msg[2])
                if len(msg) > 2:
                    self.data = list(float(data) for data in msg[3:])
                else:
                    self.data = None
        else:
            self.abort = True
