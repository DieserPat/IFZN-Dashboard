
# -*- coding: utf-8 -*-

from .PLU4000_Functions import send_serial, process_error
from .PLU4000_Venting import venting

def read_additional_parameters(serial_connection, PLU, shutoff_errors):
    # Einlasstemperatur lesen
    rx_message = send_serial(serial_connection, PLU.read_inlet_temperature)
    abort, vent = process_error(rx_message, shutoff_errors)
    PLU.respond_inlet_temperature = rx_message.respond
    if abort:
        return abort
    
    # Auslasstemperatur lesen
    rx_message = send_serial(serial_connection, PLU.read_outlet_temperature)
    abort, vent = process_error(rx_message, shutoff_errors)
    PLU.respond_outlet_temperature = rx_message.respond
    if abort:
        return abort
    
    # Einlassdruck lesen
    rx_message = send_serial(serial_connection, PLU.read_inlet_pressure)
    abort, vent = process_error(rx_message, shutoff_errors)
    PLU.respond_inlet_pressure = rx_message.respond
    if abort:
        return abort
    
    # Auslassdruck lesen
    rx_message = send_serial(serial_connection, PLU.read_outlet_pressure)
    abort, vent = process_error(rx_message, shutoff_errors)
    PLU.respond_outlet_pressure = rx_message.respond
    if abort:
        return abort

    # Temperatur und Dichte lesen
    rx_message = send_serial(serial_connection, PLU.read_density_temperature)
    abort, vent = process_error(rx_message, shutoff_errors)
    PLU.respond_density = rx_message.respond[0]
    PLU.respond_temperature = rx_message.respond[1]
    if abort:
        return abort
    
    # Digitaleingang Gasblasen lesen
    rx_message = send_serial(serial_connection, PLU.read_gas_bubbles)
    if rx_message.respond == 1:
        vent = venting(serial_connection, PLU)
        if not vent:
            return vent
    
    return abort

def standard_measurering(serial_connection, PLU, shutoff_errors):

    # if PLU.respond_statistical_measure == 0:
        # Statistik zurücksetzten
    #    send_serial(serial_connection, PLU.reset_statistic)
    #    PLU.respond_statistical_measure = 1
        # Statistik lesen 'AEDN K2 15 1 6'
    # print("--> lese neue Daten")
    rx_message = send_serial(serial_connection, PLU.read_statistical_consumption,
                            read_error=True, PLU=PLU)
    # print("--> Antwort: ", rx_message.respond)
    abort, vent = process_error(rx_message, shutoff_errors)
    if abort:
        return abort

    PLU.respond_current_measuring_number = rx_message.respond[0]
    PLU.respond_mean_value = rx_message.respond[1]
    PLU.respond_absolut_derivate = rx_message.respond[2]
    PLU.respond_relative_derivate = rx_message.respond[3]
    PLU.respond_relative_boarder = rx_message.respond[4]
    # Weitere Parameter lesen
    # print("--> Additional Parameters:")
    abort = read_additional_parameters(serial_connection, PLU, shutoff_errors)

    return abort