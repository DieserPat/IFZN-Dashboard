# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:27:36 2021

@author: gross
"""
from .class_message import Message
from .PLU4000_Functions import send_serial

class PLU_messages:

    def __init__(self,
                 variable_params,
                 fixed_params):
        """
        SERR	K2	0			Anwendungsfehler zurücksetzten
        EHRQ	K2	1	0.15	Sollwert Einlasstemperatur: Daten = Temp / 100
        ESTN	K2	1	3		Anzahl durchzuführender Messeungen. Hier: 3
        FSTN	K2	1	2		Abfrage Anzahl Messungen
        SCPA	K2	1			Temperaturregler Einlass auf Automatik (Automatik -> A, Handbetrieb -> H)
        SSTR	K2	1			Statistik zurücksetzten
        AEDN	K2	1	1	3	Anwendungsfehler 1 lesen
        EFEC	K2	2	6		Messdauer für Kraftstoffmessung.Hier: 6 Sekunden
        FFEC	K2	2	2		Messzeit Abfragen
        SCPA	K2	2			Temperaturregler Auslass auf Automatik (Automatik -> A, Handbetrieb -> H)
        SSUE	K2	2			Summierung Kraftstoffverbrauch starten
        SSUA	K2	2			Summierung Kraftstoffverbrauch stoppen
        SSUE	K2	3			Summierung Kraftstoffverbrauch gravimetrisch starten
        SSUA	K2	3			Summierung Kraftstoffverbrauch gravimetrisch stoppen
        EHRQ	K2	4	0.15	Sollwert Auslasstemperatur: Daten = Temp / 100
        AEDN	K2	5	1	3	Dichte in g/cm³ und Temperatur in °C lesen
        AEDN	K2	6	2	2	Hand-Leitrechner Schaltzustand
        AEDN	K2	6	1	3	Digitaleingang Gasblasenerkennung lesen
        EHRQ	K2	7	1		Einlasspumpen und Verbrauchsmessgerät einschalten
        EHRQ	K2	8	1		Einlasspumpe und Verbrauchsmessgerät ausschalten
        AEDN	K2	9	3	2	Entlüftungsventil Schaltzustand lesen
        AEDN	K2	9	1	2	Einlasspumpen Schaltzustand lesen
        AEDN	K2	9	2	2	Auslasspumpen Schaltzustand lesen
        EHRQ	K2	9	1		Auslasspumpen einschalten
        AEDN	K2	9	12	2	Verbrauchsmessgerät Schaltzustand lesen
        EHRQ	K2	10	1		Auslasspumpe ausschalten
        EHRQ	K2	11	1		Entlüftungsventil einschalten
        AEDN	K2	11	3	2	Auslassdruck in bar messen
        AEDN	K2	11	2	2	Einlassdruck in bar messen
        AEDN	K2	11	4	2	Rücklaufdruck in bar messen
        EHRQ	K2	12	1		Entlüftungsventil ausschalten
        AEDN	K2	13	3	2	Einlasstemperatur in °C lesen
        AEDN	K2	13	4	2	Auslasstemperatur in °C lesen
        AEDN	K2	15	1	6	Statistikergebnis volumetrischer Verbrauch in dm³/h lesen
        AEDN	K2	16	2	5	Summiertes Volumen in dm³ und andere Messwerte lesen
        AEDN	K2	16	3	5	Summiertes Masse in kg und andere Messwerte lesen
        EHRQ	K2	18	0.001	Raumausdehnungskoeefizient in 1/K
        AEDN	K2	18	1	4	Einlasstemperaturregler Zustand lesen
        AEDN	K2	18	2	4	Auslasstemperaturregler Zustand lesen
        EHRQ	K2	19	20		Wert der Temperaturkompensation in °C
        FHRQ	K2	19			Bezugstemperatur lesen
        EHRQ	K2	20	0.755	Wert der Temperaturkompensationsdichte in g/cm³
        FHRQ	K2	20			Dichte für Temperaturkompensation lesen
        EHRQ	K2	25	20		Automatische Bereichsumschaltung untere Grenze in dm³/h einstellen (hier: 20 dm³/h)
        AEDN	K2	26	2	2	Mittleren Massenverbrauch in kg/h lesen
        EHRQ	K2	26	30		Automatische Bereichsumschaltung obere Grenze in dm³/h einstellen (hier: 30 dm³/h)
        """
        self.reset_error = Message("SERR K2 0", "tx")
        self.setpoint_temp_in = Message("EHRQ K2 1 {}".format(variable_params.inlet_temperature_setpoint/100), "tx")
        self.number_of_measurements = Message("ESTN K2 1 {}".format(variable_params.set_number_of_measurements), "tx")
        self.query_NoM = Message("FSTN K2 1 2", "tx")
        self.inlet_temp_control = Message("SCP{} K2 1".format(fixed_params.temp_control_mode), "tx")
        self.reset_statistic = Message("SSTR K2 1", "tx")
        self.set_measuring_time = Message("EFEC K2 2 {}".format(variable_params.set_measuring_time), "tx")
        self.query_measuring_time = Message("FFEC K2 2", "tx")
        self.outlet_temp_control = Message("SCP{} K2 2".format(fixed_params.temp_control_mode), "tx")
        self.setpoint_temp_out = Message("EHRQ K2 4 {}".format(variable_params.outlet_temperature_setpoint/100), "tx")
        self.read_density_temperature = Message("AEDN K2 5 1 3", "tx")
        self.read_switching_state = Message("AEDN K2 6 2 2", "tx")
        self.read_gas_bubbles = Message("AEDN K2 6 1 3", "tx")
        self.start_inlet_pump = Message("EHRQ K2 7 1", "tx")
        self.stop_inlet_pump = Message("EHRQ K2 8 1", "tx")
        self.read_vent_valve_status = Message("AEDN K2 9 3 2", "tx")
        self.read_inlet_pump_status = Message("AEDN K2 9 1 2", "tx")
        self.read_outlet_pump_status = Message("AEDN K2 9 2 2", "tx")
        self.start_outlet_pump = Message("EHRQ K2 9 1", "tx")
        self.read_consumption_meter_status = Message("AEDN K2 9 12 2", "tx")
        self.stop_outlet_pump = Message("EHRQ K2 10 1", "tx")
        self.open_vent_valve = Message("EHRQ K2 11 1", "tx")
        self.read_inlet_pressure = Message("AEDN K2 11 2 2", "tx")
        self.read_outlet_pressure = Message("AEDN K2 11 3 2", "tx")
        self.read_return_pressure = Message("AEDN K2 11 4 2", "tx")
        self.close_vent_valve = Message("EHRQ K2 12 1", "tx")
        self.read_inlet_temperature = Message("AEDN K2 13 3 2", "tx")
        self.read_outlet_temperature = Message("AEDN K2 13 4 2", "tx")
        self.read_statistical_consumption = Message("AEDN K2 15 1 6", "tx")
        self.set_expansion_coefficient = Message("EHRQ K2 18 {}".format(fixed_params.expansion_coefficient), "tx")
        self.read_inlet_temperature_control = Message("AEDN K2 18 1 4", "tx")
        self.read_outlet_temperature_control = Message("AEDN K2 18 2 4", "tx")
        self.set_temperature_compensation = Message("EHRQ K2 19 {}".format(fixed_params.temperature_compensation), "tx")
        self.read_reference_temperature = Message("FHRQ K2 19", "tx")
        self.set_temperature_compensation_density = Message("EHRQ K2 20 {}".format(fixed_params.temperature_compensation_density), "tx")
        self.read_density_for_temperature_compensation = Message("FHRQ K2 20", "tx")
        self.set_automatic_range_lower_limit = Message("EHRQ K2 25 {}".format(fixed_params.range_lower_limit), "tx")
        self.set_automatic_range_upper_limit = Message("EHRQ K2 26 {}".format(fixed_params.range_upper_limit), "tx")
        
    def respond(self):
        self.respond_inlet_temperature = None
        self.respond_inlet_pressure = None
        self.respond_outlet_temperature = None
        self.respond_outlet_pressure = None
        self.respond_return_pressure = None
        self.respond_state_inlet_pump = None   
        self.respond_state_outlet_pump = None
        self.respond_state_venting_valve = None
        self.respond_gas_bubbles = None
        self.respond_current_measuring_number = None
        self.respond_mean_value = None
        self.respond_absolut_derivate = None
        self.respond_relative_derivate = None
        self.respond_relative_boarder = None
        self.respond_error_status = None
        self.respond_error_codes = None
        self.respond_error_1 = None
        self.respond_error_2 = None
        self.respond_error_3 = None
        self.respond_error_4 = None
        self.respond_error_5 = None
        self.respond_error_6 = None
        self.respond_error_7 = None
        self.respond_error_8 = None
        self.respond_error_9 = None
        self.respond_sum_volume = None
        self.respond_sum_mass = None
        self.respond_temperature_compensation = None
        self.respond_temperature_compensation_density = None
        self.respond_start_fuel_consumption = None
        self.respond_stop_fuel_consumption = None
        self.respond_average_fuel_consumption = None
        self.respond_total_fuel_consumption = None
        self.respond_temperature = None
        self.respond_density = None
        self.respond_additional_error = None
        self.respond_init = None
        self.respond_statistical_measure = None

    def application_error(self, actual_application_error):
        self.read_application_error = Message("AEDN K2 1 {} 3".format(actual_application_error), "tx")
        
        
    def change_setpoint(self, variable, setpoint, serial_connection):
        if variable == "inlet_temperature":
            self.setpoint_temp_in = Message("EHRQ K2 1 {}".format(setpoint / 1000), "tx")
            send_serial(serial_connection, self.setpoint_temp_in, setpoint / 1000)
        elif variable == "outlet_temperature":
            self.setpoint_temp_out = Message("EHRQ K2 4 {}".format(setpoint / 1000), "tx")
            send_serial(serial_connection, self.setpoint_temp_out, setpoint / 1000)
        elif variable == "number_of_measuring":
            self.number_of_measurements = Message("ESTN K2 1 {}".format(setpoint), "tx")
            send_serial(serial_connection, self.number_of_measurements, setpoint)
        elif variable == "measuring_time":
            self.set_measuring_time = Message("EFEC K2 2 {}".format(setpoint), "tx")
            send_serial(serial_connection, self.set_measuring_time, setpoint)
            
        
    def consumption(self, mode):
            if mode == "grav":
                self.start_fuel_measuring = Message("SSUE K2 3", "tx")
                self.stop_fuel_measuring = Message("SSUA K2 3", "tx")
                self.read_total_fuel = Message("AEDN K2 16 3 5", "tx")
                self.read_average_consumption = Message("AEDN K2 26 2 2", "tx")
            elif mode == "vol":
                self.start_fuel_measuring = Message("SSUE K2 2", "tx")
                self.stop_fuel_measuring = Message("SSUA K2 2", "tx")
                self.read_total_fuel = Message("AEDN K2 16 2 5", "tx")
                self.read_average_consumption = Message("AEDN K2 15 1 6", "tx")



class set_fixed_parameter:
    def __init__(self,
                 temp_control_mode,
                 expansion_coefficient,
                 temperature_compensation,
                 temperature_compensation_density,
                 range_lower_limit,
                 range_upper_limit):
        self.temp_control_mode = temp_control_mode
        self.expansion_coefficient = expansion_coefficient
        self.temperature_compensation = temperature_compensation
        self.temperature_compensation_density = temperature_compensation_density
        self.range_lower_limit = range_lower_limit
        self.range_upper_limit = range_upper_limit

class set_variable_parameter:
    def __init__(self,
                inlet_temperature_setpoint,
                outlet_temperature_setpoint,
                set_number_of_measurements,
                set_measuring_time):
        self.inlet_temperature_setpoint = inlet_temperature_setpoint
        self.outlet_temperature_setpoint = outlet_temperature_setpoint
        self.set_number_of_measurements = set_number_of_measurements
        self.set_measuring_time = set_measuring_time