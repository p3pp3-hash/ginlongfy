##!/bin/bash -x
#Run jq command to retrieve data from file domoticz-log.json and send data to domoticz;
#
#Define correct path in case the crontab does not work properly. Uncomment line below if you experience in a problem;
#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/my_raspberry_home/ginlongfy/

# Define the path to your JSON file
    JSONFile='domoticz-log.json'

# Define the Domoticz IDX, IP, and Port
    IDX_now="ID watt_now"
    IDX_day="ID kwh_day"
    IDX_total="ID kwh_total"
    IDX_month=""
    IDX_last_month=""
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
    kwh_month=$(echo "$most_recent_data" | jq -r '.kwh_month')
    kwh_lastmonth=$(echo "$most_recent_data" | jq -r '.kwh_lastmonth')


    # Check if the required data is not null
    if [ -n "$kwh_day" ] && [ -n "$watt_now" ] && [ -n "$kwh_total" ] && [ -n "$kwh_month" ] && [ -n "$kwh_lastmonth" ]; then
    
    # Print the extracted values
        echo "kwh_day: $kwh_day"
        echo "watt_now: $watt_now"
        echo "kwh_total: $kwh_total"
        echo "kwh_month: $kwh_month"
        echo "kwh_lastmonth: $kwh_lastmonth"

    # Add your code here to send the values to Domoticz

        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_now&nvalue=0&svalue=$watt_now"        
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_day&nvalue=0&svalue=$kwh_day"
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_total&nvalue=0&svalue=$kwh_total"
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_month&nvalue=0&svalue=$kwh_month"
        curl -s "http://$domoticzIP:$domoticzPort/json.htm?type=command&param=udevice&idx=$IDX_lastmonth&nvalue=0&svalue=$kwh_lastmonth"

        else
        echo "Required data not found in the JSON file."
        fi
        else
    echo "JSON file not found: $JSONFile"
fi



