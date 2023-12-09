
## Ginlongfy V0.1
First public release. 

## Ginlongfy introduction
Collect data from a second generation Ginlong/Solis inverter equipped with a WIFI stick after the discontinue support on Ginlong
Monitoring website (http://www.ginlongmonitoring.com/) without to connect to internet. The script collect data in json format and read always the last update data into the file to keep update and sync Domoticz.

## Configuring the inverter
Log into your inverter wifi stick and click on 'Advanced'
Now click 'Remote server'
Enter a new ip address for 'Server B' (your computer) enter a port number (default 9999) select 'TCP' 
Click the 'Test' button and a tick should appear.
Click 'Save' and when prompted 'Restart'

![alt text](/images/ginlong-wifi-admin.webp)

## Using the script
Open the "rd-ginlong.py" with a text editor and set the file locations for the log file and the 
webfile to suit your system. The defaults should work for a standard Linux installation. 

Once you have modified the file locations inside the file set it running. Wait for a few minutes and 
the first entry should appear when the inverter sends it's data. You may have to disable/modify any
running firewall on your system.

## The output files
The log file 'domoticz-log.json' contains following values separated as follows:

{
    "kwh_day": 8.8, 
    "kwh_month": 12, 
    "ac_amps": 4.0, 
    "timestamp": "2023-12-02 10:01", 
    "kwh_yesterday": 3.0, 
    "kwh_lastmonth": 133, 
    "dc_volts2": 0.0, 
    "dc_amps1": 3.7, 
    "dc_amps2": 0.0, 
    "temp": 27.6, 
    "ac_volts": 244.8, 
    "ac_freq": 49.95, 
    "kwh_total": 7538.0, 
    "watt_now": 979, 
    "dc_volts1": 246.6
}

The script 'upldata.sh' will read and push data in Domoticz to update sensors. Use crontab -e in your linux machine to automate the job in Domoticz.

## Disclaimer
This works fine on my Solis 3.6 2G inverter equipped with a WIFI 'stick'. According to Ginlong, the 
WIFI stick is compatible with all it's current solar and wind generation 2G inverters. It would be
logical therefore to assume that these scripts would be compatible with all the current second
generation inverters. The simple fact is that I only have one inverter installed and these scripts
work for me! Please feel free to try them on other Ginlong inverters and let me know how you get on,
please.

Thanks to graham0 for original code "https://github.com/graham0/ginlong-wifi".
