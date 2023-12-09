##!/bin/bash -x
#Define correct path in case the crontab does not work properly. Uncomment line below;
#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/my_raspberry_home/ginlongfy/

# Define the path to your JSON file
JSONFile='domoticz-log.json'

# Define the Domoticz IDX, IP, and Port
IDX="ID watt_now"
IDX_1="ID kwh_day"
IDX_2="ID kwh_total"
domoticzIP='localhost or your domoticz IP'
domoticzPort="your domoticz port"

# Check if the JSON file exists
if [ -e "$JSONFile" ]; then
    # Extract the most recent data using jq and sort
    most_recent_data=$(jq -s 'max_by(.timestamp)' "$JSONFile")

    # Extract the required data
    kwh_day=$(echo "$most_recent_data" | jq -r '.kwh_day')
    watt_now=$(echo "$most_recent_data" | jq -r '.watt_now')
    kwh_total=$(echo "$most_recent_data" | jq -r '.kwh_total')

    # Check if the required data is not null
    if [ -n "$kwh_day" ] && [ -n "$watt_now" ] && [ -n "$kwh_total" ]; then
        # Print the extracted values
        echo "kwh_day: $kwh_day"
        echo "watt_now: $watt_now"
        echo "kwh_total: $kwh_total"

        # Add your code here to send the values to Domoticz

        # Example: Send the values to Domoticz using curl
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX&nvalue=0&svalue=$watt_now"        
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_1&nvalue=0&svalue=$kwh_day"
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_2&nvalue=0&svalue=$kwh_total"
    
else
        echo "Required data not found in the JSON file."
    fi
else
    echo "JSON file not found: $JSONFile"
fi



