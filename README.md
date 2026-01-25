
## Ginlongfy (offline)
Reader for second‑gen Ginlong/Solis inverters with Wi‑Fi stick after the cloud shutdown. Listens locally, decodes the packet, logs JSON, and updates Domoticz without jq or shell glue.

![alt text](/images/wifi-stick.webp)

## Configure the inverter
1. Log into the Wi‑Fi stick, open **Advanced → Remote server**.  
2. Set **Server B** to your machine IP and port (default `9999`), protocol `TCP`.  
3. Click **Test**, then **Save** and reboot the stick.

![alt text](/images/ginlong-wifi-admin.webp)

## Run the script
- Edit `ginlong_local.py` and set `DOMOTICZ_BASE` and the IDX values you use in Domoticz.  
- Optional: adjust `PORT`, `POWER_MULTIPLIER` (set to `10` if power reads 10× too low), and log paths.
- Start it: `python3 ginlong_local.py`. Wait for the next packet (about every 7 minutes).

## Output
- Latest reading: `domoticz-latest.json`
- History (JSON Lines): `domoticz-log.jsonl`
- Domoticz: sends `watt;total_kWh` to `IDX_COMBINED`, plus optional day/month/last month/power-only IDX if set.

Example JSON (one line in the history file):
```
{"timestamp":"2023-12-02 10:01","watt_now":979,"kwh_day":8.8,"kwh_total":7538.0,"dc_volts1":246.6,"dc_volts2":0.0,"dc_amps1":3.7,"dc_amps2":0.0,"ac_volts":244.8,"ac_amps":4.0,"ac_freq":49.95,"kwh_yesterday":3.0,"kwh_month":12,"kwh_lastmonth":133,"temp":27.6}
```

## Notes
- The stick typically reports every ~7 minutes; the script logs immediately and overwrites `domoticz-latest.json` so you can read the last value without `jq`.
- Older scripts (`ginlong.py`, `rd-ginlong.py`, `upldata.sh`) are kept for reference but no longer required.

## Thanks
Thanks to graham0 for the original code: https://github.com/graham0/ginlong-wifi.
