# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 10:06:27 2022

@author: gross
"""
import serial

def connect_serial(port, baudrate=9600):
    """
    Parameters
    ----------
    port : string
        The port of the used serial communication.

    Returns
    -------
    serial object
        Returns the serial modul, which must be used to read and write bytes, or None
        if no connection is etablishes.
    bool
        Return True, if a connactions is etablished. False if not.        

    """
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
    
# port = "com4"
# baudrate=9600
# ser = serial.Serial(port=port.upper(),baudrate=baudrate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout= 1)