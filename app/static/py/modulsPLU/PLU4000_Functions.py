# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 14:37:00 2021

@author: gross
"""


"""Skript für eine RS232-Kommunikation zwischen der Kraftstoffwaage PLU400
und einem RaspberryPi zur Siganlübertragung der Messdaten und 
Stellgrößen.
Die Messdaten werden anschließend vom RPi mittels UDP an
die MAB gesendet. Zusätzlich können Stellgrößen und Messbefehle von der
MAB an den RPi gesendet werden.

Werkseinstellungen der PLU4000:
    - 9600 Baud,
    - 8 Bit,
    - Keine Parität,
    - 1 Stopbit,
    - Kein XON / XOFF-Protokoll,
    - kein Hardwareprotokoll.
    
Die Liste der AK-Befehle inklusive ihrer Beschreibung liegt unter:
    Link!

AK-Protokoll:
    Bei der Eingabe müssen für die Startmarke, Pause und Endmarke folgende
    Tastenkommandos eingegeben werden:
        - STX: ASCII-Code für Start einer Nachricht (Hex 02, Strg B, ^B)
        - SPC: ASCII-Code für Leerzeichen (wird mir "_" gekennzeichnet)
        - ETX: ASCII-Code für Ende einer Nachricht (Hex 03, Strg C, ^C)
        - Kanalnummer "K": darstellbares ASCII-Zeichen
        - a: Großbuchstabe
        - i: Ziffer
        - c: a oder i
    Startmarke  Pause   Funktionscode   Pause   Kanalnummer     Daten  ... 
    STX         SPC     acc             SPC     "K"iii          ...    ... 
    Pause   Endmarke
    SPC     ETX
    -> Beispiel: ^B_AEDN_K2_39_1_2_^C
    
    Quitutungstelegramm vom PLU4000:
    Startmarke  Pause   Funktionscode   Pause   Fehlerstatus    Pause   ...
    STX         SPC     acc             SPC        i            SPC     ...
    Kanalnummer     Sonderstatus    Daten   Pause   Endmarke
    "K"iii          aa              ...     SPC     ETX
    -> Beispiel: ^B_AEDN_0_K2_OK_39_1_2_1258.5431_56.4438_^C
    
    Als Kanalnummer ist immer die "2" voreingestellt.
"""

import pandas as pd
from time import sleep
from .class_message import Message


def send_serial_message(serial_connector, tx_message):
    serial_connector.write("\x02 {} \x03".format(tx_message.message).encode())
    # print(tx_message.message)
    try:
        msg = serial_connector.read_until(b"\x03").decode()
        rx = process_messages(tx_message, Message(msg, "rx"))
        # print(rx.respond)
        flag = True
    except:
        rx = Message("", "rx", no_rx=True)
        flag = False
    return flag, rx


def send_serial(serial_connector, tx_message, expected_respond=None,
                second_msg=None, read_error=False, PLU=None):
    flagRX, rx_message = send_serial_message(serial_connector, tx_message)
    if flagRX:
        if rx_message.checksum == 0 or rx_message.checksum == 3:
            rx_message = resend(serial_connector, tx_message, expected_respond, second_msg)
        elif rx_message.checksum == 2:
            if read_error:
                # print("--> Lese Fehler")
                rx_message.error = read_error_status(serial_connector, rx_message, tx_message, PLU)
            else:
                pass
        elif rx_message.checksum == 1:
            if expected_respond and type(rx_message.respond) is not str:
                if float(rx_message.respond) != float(expected_respond):
                    rx_message = resend(serial_connector, tx_message, expected_respond, second_msg)
    else:
        rx_message.abort = True
    return rx_message


def load_error_code():
    """function to load the table with the error codes
    Input: None; the used path is described below and should never change
    Output: pandas DataFrame with the codes; error status as index and description as data"""
    path_error_codes = r"app/static/notes/error_codes.txt"
    raw_data = pd.read_csv(path_error_codes, sep="\t")
    error_codes = pd.DataFrame({"Bedeutung": raw_data["Bedeutung"],
                                "Message": raw_data["Message"]})
    # change the "NA"-status back to "NA"; pandas changes it automatically to "nan"
    for i, status in enumerate(raw_data["Status"]):
        if str(status) == "nan":
            raw_data["Status"][i] = "NA"
    # set the status as index of the DataFrame
    error_codes.index = raw_data["Status"]
    # and rename the index to "Status"
    error_codes.index.name = "Status"
    return error_codes


def process_messages(tx_message, rx_message):
    """function to process the messages
    Input:  tx_message: class-type 'Message'
            rx_message: class-type 'Message'
            error_codes: DataFrame with the error-codes
            application_error: DataFrame with the application-error-codes
    Output: data: the received data from the fuel scale
            checksum: information for further steps
    """

    def sort_data(rx, tx):
        """function to sort the received data by deleting the send data to get the real-received data
        Input:  rx_data: list
                tx_data: list
        Output: new_data: sorted"""
        AZ = 0
        respond = None
        if len(rx.data) == len(tx.data):
            corr_data = True
            if len(rx.data) == 0:
                if rx.task == 0:
                    respond = rx.task
                else:
                    respond = rx.function_code[-1]
            else:
                respond = rx.data[-1]
        else:
            if rx.data[:2] == tx.data[:2]:
                corr_data = True
                AZ = rx.data[2]
                if len(rx.data[3:]) == 1:
                    respond = rx.data[3]
                elif len(rx.data[3:]) == 2 and rx.task == 6:
                    respond = rx.data[4]
                else:
                    respond = rx.data[3:]
            else:
                corr_data = False
        return AZ, respond, corr_data

    if tx_message.function_code == rx_message.function_code and tx_message.task == rx_message.task:
        AZ, respond, corr_data = sort_data(rx_message,tx_message)
        # compare, if the send and received function-code is the same;
        # this should give information, if the answer is correct to the request
        if rx_message.error_status == 0 and rx_message.error_code == "OK" and corr_data:
            # there is no error-status and the error-code is "OK"
            rx_message.checksum = 1
            rx_message.AZ, rx_message.respond = AZ, respond
            return rx_message
        elif rx_message.error_status != 0 and rx_message.error_code == "OK" and corr_data:
            # there is at least one error-status but the error-code is "OK"
            rx_message.checksum = 2
            rx_message.AZ, rx_message.respond = AZ, respond
            return rx_message
        elif rx_message.error_code != "OK":
            # the error-code is not "OK"
            rx_message.checksum, rx_message.AZ, rx_message.respond = (
                3, None, load_error_code().loc[rx_message.error_code]["Message"])
            return rx_message
        else:
            # nothing of the above is true
            rx_message.checksum, rx_message.AZ, rx_message.respond = (
                0, None, None)
            return rx_message
    else:
        # the function-code of the send and received message is not the same
        rx_message.checksum, rx_message.AZ, rx_message.respond = (
            0, None, None)
        return rx_message


def resend(serial_connection, tx_message, expected_respond, second_message=None):
    count = 0
    flag, rx_message = send_serial_message(serial_connection, tx_message)
    while rx_message.respond != expected_respond:
        count += 1
        if second_message:
            send_serial_message(serial_connection, second_message)
            flag, rx_message = send_serial_message(serial_connection, tx_message)
        else:
            flag, rx_message = send_serial_message(serial_connection, tx_message)
        if rx_message.respond == expected_respond:
            break
        if count == 2:
            rx_message.abort = True
            break
        sleep(0.5)
    return rx_message


def read_error_status(serial_connector, rx_message, tx_message, PLU):
    def translate_application_error(task_eds, application_error):
        """function to read the received application error
        Input:  task: int; the task-number
                eds: int; the eds-number
                application_error: DataFrame; the application-errors
        Output: str; the description of the error"""
        task, eds = int(task_eds[0]), int(task_eds[1])
        df = application_error[application_error["Task"] == task]
        df = df[df["EDS"] == eds]
        return df["Message"].loc[df.index[0]]

    error = list()
    path_codes = r"app/static/notes/appli_error.txt"
    application_error = pd.read_csv(path_codes, sep=",")
    # print("--> Anzahl Fehler: ", rx_message.error_status)
    for i in range(rx_message.error_status):
        # print("--> Fehler nummer ", i+1)
        PLU.application_error(i+1)
        flag, rx_msg = send_serial_message(serial_connector, PLU.read_application_error)
        app_error = translate_application_error(rx_msg.respond, application_error)
        # print("***** Error! *****")
        # print(rx_msg.respond)
        # print(app_error)
        if app_error not in error:
            error.append(app_error)
    send_serial_message(serial_connector, PLU.reset_error)

    return error

def process_error(rx_message, shutoff_errors):
    vent = False
    shutdown = False
    if rx_message.error_status != 0 and rx_message.error is not None:
        for error in rx_message.error:
            if error in shutoff_errors:
                shutdown = True
                return shutdown, vent
            elif error == 2:
                vent = True
    return shutdown, vent
