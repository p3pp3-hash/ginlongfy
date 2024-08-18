
## Ginlongfy V1.0
What's new: minors bugfix and improvements to the script.

## Ginlongfy introduction
Collect data from a second generation Ginlong Wind and Solar Inverter equipped with a WIFI stick after the discontinue support on Ginlong
Monitoring website (http://www.ginlongmonitoring.com/) without to connect to internet. The script collect data in json format and read always the last update data into the file to keep update and sync Domoticz.

![alt text](/images/wifi-stick.webp)

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

![alt text](/images/domoticz.png)

## The back-up function
You can back-up your log using the file 'json-backup.sh', this will reduce your log file, in case you don't wnat keep it too long.



## Disclaimer
This works fine on Ginlong Wind and Solar Inverter equipped with a WIFI 'stick'. According to Ginlong, the WIFI stick is compatible with all it's current solar and wind generation 2G inverters. Please feel free to try them on other Ginlong inverters and let me know how you get on, please.

Thanks to graham0 for original code "https://github.com/graham0/ginlong-wifi".
