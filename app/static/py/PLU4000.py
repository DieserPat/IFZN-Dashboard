# import .modulsPLU.PLU4000_Functions as mf
from .modulsPLU.PLU4000_Messages import PLU_messages, set_variable_parameter, set_fixed_parameter
from .modulsPLU.PLU4000_Initialize import init_PLU4000
# from .modulsPLU.PLU4000_Consumption_Measure import read_fuel_consumption
from .modulsPLU.PLU4000_Statistical_Measure import standard_measurering
from .modulsPLU.PLU4000_Start_Stop import start_PLU4000, stop_PLU4000
from .modulsPLU.PLU4000_Start_Connection import connect_serial


def setMessage(
    inlet_temperature_setpoint = 20,
    outlet_temperature_setpoint = 20,
    set_number_of_measurements = 6,
    set_measuring_time = 3):
    # Variables
    variable_params = set_variable_parameter(
        inlet_temperature_setpoint = inlet_temperature_setpoint,
        outlet_temperature_setpoint = outlet_temperature_setpoint,
        set_number_of_measurements = set_number_of_measurements,
        set_measuring_time = set_measuring_time)
    #  *** Fixed Variables ***
    # Parameters, which will remain the same (For diesel-fuel!)
    fixed_params = set_fixed_parameter(
        temp_control_mode="A",
        expansion_coefficient=0.001,
        temperature_compensation=20,
        temperature_compensation_density=0.755,
        range_lower_limit=20,
        range_upper_limit=30)
    PLU = PLU_messages(variable_params=variable_params,
                        fixed_params=fixed_params)
    PLU.respond()
    return PLU

def initialize(serial_port, PLU):
    ser, ser_conn = connect_serial(serial_port)
    init = False
    if ser_conn:
        # try:
        init = init_PLU4000(ser, PLU)
        # except:
        #     pass
        ser.close()
    return init

def start(serial_port, PLU, shutoff_error):
    ser, ser_conn = connect_serial(serial_port)
    startPump = False
    if ser_conn:
        try:
            startPump = start_PLU4000(ser, PLU, shutoff_error)
        except:
            pass
        ser.close()
    return startPump

def stop(serial_port, PLU):
    ser, ser_conn = connect_serial(serial_port)
    stopPump = False
    if ser_conn:
        try:
            stopPump = stop_PLU4000(ser, PLU)
        except:
            pass
        ser.close()
    return stopPump

def statMeasurment(serial_port, PLU, shutoff_error):
    ser, ser_conn = connect_serial(serial_port)
    if ser_conn:
        try:
            standard_measurering(ser, PLU, shutoff_error)
        except:
            pass
        ser.close()