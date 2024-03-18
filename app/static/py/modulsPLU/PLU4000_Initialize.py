# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 15:05:34 2021

@author: gross
"""

from .PLU4000_Functions import send_serial


def init_PLU4000(serial_connection, PLU):
    # Handleitrechner Schaltzustand lesen
    rx_message = send_serial(serial_connection, PLU.read_switching_state, 0, PLU.read_switching_state)
    while not rx_message.abort:
        # Sollwert Einlasstemperatur
        rx_message = send_serial(serial_connection, PLU.setpoint_temp_in, PLU.setpoint_temp_in)
        if rx_message.abort:
            break
        # Sollwert Auslasstemperatur
        rx_message = send_serial(serial_connection, PLU.setpoint_temp_out, PLU.setpoint_temp_out)
        if rx_message.abort:
            break
        # Sollwert Raumausdehnungskoeffizient
        rx_message = send_serial(serial_connection, PLU.set_expansion_coefficient,
                                    PLU.set_expansion_coefficient)
        if rx_message.abort:
            break
        # Sollwert Temperaturkompensation
        rx_message = send_serial(serial_connection, PLU.set_temperature_compensation,
                                    PLU.set_temperature_compensation)

        PLU.respond_temperature_compensation = rx_message.respond
        if rx_message.abort:
            break
        # Sollwert Temperaturkompensationsdichte
        rx_message = send_serial(serial_connection, PLU.set_temperature_compensation_density,
                                    PLU.set_temperature_compensation_density)
        PLU.respond_temperature_compensation_density = rx_message.respond
        if rx_message.abort:
            break
        # Anzahl Messungen vorgeben
        rx_message = send_serial(serial_connection, PLU.number_of_measurements, PLU.number_of_measurements)
        if rx_message.abort:
            break
        # Messdauer vorgeben
        rx_message = send_serial(serial_connection, PLU.set_measuring_time, PLU.set_measuring_time)
        if rx_message.abort:
            break
        # Einlasstemperaturregler auf Automatikbetrieb stellen
        rx_message = send_serial(serial_connection, PLU.inlet_temp_control, PLU.inlet_temp_control)
        if rx_message.abort:
            break
        # Auslasstemperaturregler auf Automatikbetrieb stellen
        rx_message = send_serial(serial_connection, PLU.outlet_temp_control, PLU.outlet_temp_control)
        if rx_message.abort:
            break
        # Entlüftungsventil-Schaltzustand lesen
        rx_message = send_serial(serial_connection, PLU.read_vent_valve_status, 0, PLU.close_vent_valve)
        PLU.respond_gas_bubbles = rx_message.respond
        if rx_message.abort:
            break
        # Einlasspumpen-Schaltzustand lesen
        rx_message = send_serial(serial_connection, PLU.read_inlet_pump_status, 0, PLU.stop_inlet_pump)
        PLU.respond_state_inlet_pump = rx_message.respond
        if rx_message.abort:
            break
        # Auslasspumpen-Schaltzustand lesen
        rx_message = send_serial(serial_connection, PLU.read_outlet_pump_status, 0, PLU.stop_outlet_pump)
        PLU.respond_state_outlet_pump = rx_message.respond
        if rx_message.abort:
            break
        rx_message = send_serial(serial_connection, PLU.reset_error)
        # Wenn Initialisierung erfolgreich, respond und "True" zurückgeben
        return True
   # Wenn Initialisierung nicht erfolgreich, respond und "False" zurückgeben
    return False
    

