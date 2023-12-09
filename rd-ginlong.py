import socket
import binascii
import time
import json

# Change these values to suit your requirements:
HOST = ''  # Hostname or IP address of the interface, leave blank for all
PORT = 9999  # Listening on port 9999
domoticz_logfile = 'domoticz-log.json'  # Location of the Domoticz log file

# Inverter values found (so far), all big endian 16-bit unsigned:
header = '685951b0'  # Hex stream header
data_size = 206  # Hex stream size
inverter_temp = 31
inverter_vdc1 = 33
inverter_vdc2 = 35
inverter_adc1 = 39
inverter_adc2 = 41
inverter_aac = 45
inverter_vac = 51
inverter_freq = 57
inverter_now = 59
inverter_yes = 67
inverter_day = 69
inverter_tot = 71
inverter_mth = 87
inverter_lmth = 91

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

while True:
    sock.listen(1)
    conn, addr = sock.accept()
    rawdata = conn.recv(1000)
    hexdata = binascii.hexlify(rawdata)

    if (hexdata[0:8] == header and len(hexdata) == data_size):
        watt_now = str(int(hexdata[inverter_now * 2:inverter_now * 2 + 4], 16))
        kwh_day = str(float(int(hexdata[inverter_day * 2:inverter_day * 2 + 4], 16)) / 100)
        kwh_total = str(int(hexdata[inverter_tot * 2:inverter_tot * 2 + 8], 16) / 10)
        temp = str(float(int(hexdata[inverter_temp * 2:inverter_temp * 2 + 4], 16)) / 10)
        dc_volts1 = str(float(int(hexdata[inverter_vdc1 * 2:inverter_vdc1 * 2 + 4], 16)) / 10)
        dc_volts2 = str(float(int(hexdata[inverter_vdc2 * 2:inverter_vdc2 * 2 + 4], 16)) / 10)
        dc_amps1 = str(float(int(hexdata[inverter_adc1 * 2:inverter_adc1 * 2 + 4], 16)) / 10)
        dc_amps2 = str(float(int(hexdata[inverter_adc2 * 2:inverter_adc2 * 2 + 4], 16)) / 10)
        ac_volts = str(float(int(hexdata[inverter_vac * 2:inverter_vac * 2 + 4], 16)) / 10)
        ac_amps = str(float(int(hexdata[inverter_aac * 2:inverter_aac * 2 + 4], 16)) / 10)
        ac_freq = str(float(int(hexdata[inverter_freq * 2:inverter_freq * 2 + 4], 16)) / 100)
        kwh_yesterday = str(float(int(hexdata[inverter_yes * 2:inverter_yes * 2 + 4], 16)) / 100)
        kwh_month = str(int(hexdata[inverter_mth * 2:inverter_mth * 2 + 4], 16))
        kwh_lastmonth = str(int(hexdata[inverter_lmth * 2:inverter_lmth * 2 + 4], 16))
        timestamp = (time.strftime("%F %H:%M"))

        # Create a dictionary to store the data in JSON format
        data = {
            "timestamp": timestamp,
            "watt_now": int(watt_now),
            "kwh_day": float(kwh_day),
            "kwh_total": float(kwh_total),
            "dc_volts1": float(dc_volts1),
            "dc_volts2": float(dc_volts2),
            "dc_amps1": float(dc_amps1),
            "dc_amps2": float(dc_amps2),
            "ac_volts": float(ac_volts),
            "ac_amps": float(ac_amps),
            "ac_freq": float(ac_freq),
            "kwh_yesterday": float(kwh_yesterday),
            "kwh_month": int(kwh_month),
            "kwh_lastmonth": int(kwh_lastmonth),
            "temp": float(temp)
        }

        # Serialize the data to JSON format
        data_json = json.dumps(data, indent=4)

        # Write the JSON data to the Domoticz log file (domoticz-log.json)
        with open(domoticz_logfile, 'a') as domoticz_log:
            domoticz_log.write(data_json + '\n')

conn.close()

    
