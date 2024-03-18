# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 17:43:50 2021

@author: gross
"""

from .PLU4000_Functions import send_serial
from time import sleep

def venting(serial_connection, PLU):
    # Schaltzustand lesen
    rx_message = send_serial(serial_connection, PLU.read_vent_valve_status)
    PLU.respond_state_venting_valve = rx_message.respond
    # Wenn Ventil geschlossen ist, Entlüftungsventil öffnen
    if int(rx_message.respond) == 0:
        rx_message = send_serial(serial_connection, PLU.open_vent_valve, 1)
        rx_message = send_serial(serial_connection, PLU.read_vent_valve_status, 1, PLU.open_vent_valve)
        PLU.respond_state_venting_valve = rx_message.respond
        if rx_message.abort:
            send_serial(serial_connection, PLU.close_vent_valve, 1)
            PLU.respond_additional_error = 4
            return False
        else:
            sleep(1)
            rx_message = send_serial(serial_connection, PLU.close_vent_valve, 1)
            rx_message = send_serial(serial_connection, PLU.read_vent_valve_status, 0, PLU.close_vent_valve)
            PLU.respond_state_venting_valve = rx_message.respond
            if rx_message.abort:
                PLU.respond_additional_error = 4
                return False
            else:
                send_serial(serial_connection, PLU.reset_error)            
                return True