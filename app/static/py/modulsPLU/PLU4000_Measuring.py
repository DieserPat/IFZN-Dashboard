# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 14:28:34 2021

@author: gross
"""

import moduls.PLU4000_Functions as mf
from moduls.PLU4000_Start_Stop import stop_PLU4000
from moduls.PLU4000_Venting import venting



    

def standard_measurering(serial_connection, PLU, send_array, UDP, UDP_send_order, 
                         prev_UDP_msg, addr, shutoff_errors):
    abort = False
    # Statistik zurücksetzten
    mf.send_serial(serial_connection, PLU.reset_statistic)
    UDP_msg, PLU = mf.read_ethernet(UDP, prev_UDP_msg, PLU, serial_connection)
    while UDP_msg.task == 4 or UDP_msg.task == 2:
        # Statisktik lesen
        rx_message = mf.send_serial(serial_connection, PLU.read_statistical_consumption,
                                     read_error=True, PLU=PLU)
        send_array, abort = process_error(serial_connection, rx_message, shutoff_errors, send_array,
                  PLU, UDP_send_order)
        UDP_msg, PLU = mf.read_ethernet(UDP, prev_UDP_msg, PLU, serial_connection)
        if abort or (UDP_msg.task != 4 and UDP_msg.task != 2):
            break
        send_array[UDP_send_order.current_measuring_number] = rx_message.respond[0]
        send_array[UDP_send_order.mean_value] = rx_message.respond[1] * 10000
        send_array[UDP_send_order.absolut_derivate] = rx_message.respond[2] * 100
        send_array[UDP_send_order.relative_derivate] = rx_message.respond[3] * 10000
        send_array[UDP_send_order.relative_boarder] = rx_message.respond[4] * 10000
        mf.send_UDP(UDP, send_array, addr)
        
        # Weitere Parameter lesen
        send_array, abort, UDP_msg = read_additonal_parameters(serial_connection, PLU, send_array, UDP, UDP_send_order,
                                                      prev_UDP_msg, addr, shutoff_errors)
        if abort or (UDP_msg.task != 4 and UDP_msg.task != 2):
            break
    
    return send_array, abort, UDP_msg
        

def read_fuel_consumption(serial_connection, PLU, send_array, UDP, UDP_send_order,
                          prev_UDP_msg, addr, shutoff_errors):
    abort = False
    # Statistik zurücksetzten
    mf.send_serial(serial_connection, PLU.reset_statistic)
    UDP_msg = prev_UDP_msg
    mode = 5
    if UDP_msg.task == 5:
        PLU.consumption("vol")
    elif UDP_msg.task == 6:
        mode = 6
        PLU.consumption("grav")
    # Summierung Kraftstoffverbrauch starten
    rx_message = mf.send_serial(serial_connection, PLU.start_fuel_measuring)
    send_array[UDP_send_order.start_fuel_consumption] = 1
    send_array[UDP_send_order.stop_fuel_consumption] = 0
    mf.send_UDP(UDP, send_array, addr)
    
    while mode == UDP_msg.task:
        # Durchschnittlichen Kraftstoffverbrauch messen
        rx_message = mf.send_serial(serial_connection, PLU.read_average_consumption)
        if mode == 5:
            send_array[UDP_send_order.average_fuel_consumption] = rx_message.respond[0]
        else:
            send_array[UDP_send_order.average_fuel_consumption] = rx_message.respond
        # Totalen Kraftstoffverbrauch messen
        rx_message = mf.send_serial(serial_connection, PLU.read_total_fuel)
        send_array[UDP_send_order.total_fuel_consumption] = rx_message.respond[0]
        mf.send_UDP(UDP, send_array, addr)
        UDP_msg, PLU = mf.read_ethernet(UDP, prev_UDP_msg, PLU, serial_connection)
        if abort or mode != UDP_msg.task:
            break
        # Weitere Parameter lesen
        send_array, abort, UDP_msg = read_additonal_parameters(serial_connection, PLU, send_array, UDP, UDP_send_order,
                                                      prev_UDP_msg, addr, shutoff_errors)
        # UDP_msg, PLU = mf.read_ethernet(UDP, prev_UDP_msg, PLU, serial_connection)
        if abort or mode != UDP_msg.task:
            break
    else:
        # Summeriung Kraftstoffverbrauch stoppen
        rx_message = mf.send_serial(serial_connection, PLU.stop_fuel_measuring)
        send_array[UDP_send_order.start_fuel_consumption] = 0
        send_array[UDP_send_order.stop_fuel_consumption] = 1
        # Durchschnittlichen Kraftstoffverbrauch messen
        rx_message = mf.send_serial(serial_connection, PLU.read_average_consumption)
        send_array[UDP_send_order.average_fuel_consumption] = rx_message.respond
        # Totalen Kraftstoffverbrauch messen
        rx_message = mf.send_serial(serial_connection, PLU.read_total_fuel)
        send_array[UDP_send_order.total_fuel_consumption] = rx_message.respond
        mf.send_UDP(UDP, send_array, addr)
        
    
    return send_array, abort, UDP_msg
        