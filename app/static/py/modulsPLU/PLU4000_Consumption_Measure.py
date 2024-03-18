# -*- coding: utf-8 -*-

from moduls.PLU4000_Functions import send_serial, read_additional_parameters

def read_fuel_consumption(serial_connection, PLU, shutoff_errors, active, vol=True):
    if active:
        if PLU.respond_start_fuel_consumption == 1:
            # Durchschnittlichen Kraftstoffverbrauch messen
            rx_message = send_serial(serial_connection, PLU.read_average_consumption)
            if vol:
                PLU.respond_average_fuel_consumption = rx_message.respond[0]
            else:
                PLU.respond_average_fuel_consumption = rx_message.respond
            # Totalen Kraftstoffverbrauch messen
            rx_message = send_serial(serial_connection, PLU.read_total_fuel)
            PLU.respond_total_fuel_consumption = rx_message.respond[0]
            if rx_message.abort:
                return PLU, False
            # Weitere Parameter lesen
            PLU, abort = read_additional_parameters(serial_connection, PLU, shutoff_errors)
            if abort:
                return PLU, False
        else:
            # Statistik zurücksetzten
            send_serial(serial_connection, PLU.reset_statistic)
            if vol:
                PLU.consumption("vol")
            else:
                PLU.consumption("grav")
            # Summierung Kraftstoffverbrauch starten
            rx_message = send_serial(serial_connection, PLU.start_fuel_measuring)
            PLU.respond_start_fuel_consumption = 1
            PLU.respond_stop_fuel_consumption = 0
        
    else:
        # Summeriung Kraftstoffverbrauch stoppen
        rx_message = send_serial(serial_connection, PLU.stop_fuel_measuring)
        PLU.respond_start_fuel_consumption = 0
        PLU.respond_stop_fuel_consumption = 1
        # Durchschnittlichen Kraftstoffverbrauch messen
        rx_message = send_serial(serial_connection, PLU.read_average_consumption)
        PLU.respond_average_fuel_consumption = rx_message.respond
        # Totalen Kraftstoffverbrauch messen
        rx_message = send_serial(serial_connection, PLU.read_total_fuel)
        PLU.respond_total_fuel_consumption = rx_message.respond        
    
    return PLU, True