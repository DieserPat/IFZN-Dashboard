# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 10:43:25 2021

@author: IFZN_TH_Nürnberg

"""
from .PLU4000_Functions import send_serial

def stop_inlet_pump(serial_connection, PLU):
    # Einlasspumpen und Verbrauchsmessgerät ausschalten
    send_serial(serial_connection, PLU.stop_inlet_pump, 1)
    # Zustand lesen
    rx_message = send_serial(serial_connection, PLU.read_inlet_pump_status, 0, PLU.stop_inlet_pump)
    PLU.respond_state_inlet_pump = rx_message.respond
    PLU.state_inlet_pump = rx_message.respond


def stop_outlet_pump(serial_connection, PLU):
    # Auslasspumpe ausschalten
    send_serial(serial_connection, PLU.stop_outlet_pump, 1)
    # Zustand lesen
    rx_message = send_serial(serial_connection, PLU.read_outlet_pump_status, 0, PLU.stop_outlet_pump)
    PLU.respond_state_outlet_pump = rx_message.respond
    PLU.state_outlet_pump = rx_message.respond
    

def start_PLU4000(serial_connection, PLU, shutoff_error):
    # Einlasspumpen und Verbrauchsmessgerät einschalten
    rx_message = send_serial(serial_connection, PLU.start_inlet_pump, 1, PLU=PLU)
    if not rx_message.abort:
        # Zustand lesen
        rx_message = send_serial(serial_connection, PLU.read_inlet_pump_status, 1, PLU.start_inlet_pump,
                                    read_error=True, PLU=PLU)
        PLU.state_inlet_pump = rx_message.respond
        PLU.respond_state_inlet_pump = rx_message.respond
        if rx_message.error and [error for error in rx_message.error if error in shutoff_error]:
            stop_inlet_pump(serial_connection, PLU)
            return False
        elif rx_message.abort:
            stop_inlet_pump(serial_connection, PLU)
            PLU.additional_error = 2
            PLU.respond_additional_error = 2
            return False
        else:
            # Auslasspumpe einschalten
            rx_message = send_serial(serial_connection, PLU.start_outlet_pump, 1, PLU=PLU)
            # Zustand lesen
            rx_message = send_serial(serial_connection, PLU.read_outlet_pump_status, 1, PLU.start_outlet_pump,
                                        read_error=True, PLU=PLU)
            PLU.state_outlet_pump = rx_message.respond
            PLU.respond_state_outlet_pump = rx_message.respond
            if rx_message.error and [error for error in rx_message.error if error in shutoff_error]:
                stop_inlet_pump(serial_connection, PLU)
                stop_outlet_pump(serial_connection, PLU)
                return False
            elif rx_message.abort:
                stop_outlet_pump(serial_connection, PLU)
                stop_inlet_pump(serial_connection, PLU)
                PLU.additional_error = 3
                PLU.respond_additional_error = 3
                return False
    return True


def stop_PLU4000(serial_connection, PLU):
    #send_array[UDP_send_order.state_outlet_pump] = rx_message.respond
    stop_inlet_pump(serial_connection, PLU)
    stop_outlet_pump(serial_connection, PLU)
    # Entlüftungsventil schließen, falls dieses geöffnet ist
    rx_message = send_serial(serial_connection, PLU.read_vent_valve_status, 0, PLU.close_vent_valve)
    PLU.respond_state_venting_valve = rx_message.respond
    return True