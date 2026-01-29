#!/usr/bin/env python3
"""Offline reader for Ginlong/Solis Wi-Fi sticks with Domoticz push.

Listens on the local TCP port configured as Server B on the stick, decodes the
telemetry packet, stores the latest reading, keeps a JSONL history, and pushes
selected fields to Domoticz without jq or shell scripts.
"""

import binascii
import json
import logging
import socket
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Network listener (Server B on the Wi-Fi stick must point here)
HOST = ""  # Listen on all interfaces
PORT = 9999

# Packet validation
HEADER_HEX = "685951b0"
EXPECTED_HEX_LEN = 206  # hex string length of the full packet

# Scaling tweaks (set to 10 if your power reads 150 instead of 1500 W, etc.)
POWER_MULTIPLIER = 1

# Logging
LOG_LATEST = Path("domoticz-latest.json")
LOG_HISTORY = Path("domoticz-log.jsonl")  # JSON Lines (one object per line)

# Domoticz
DOMOTICZ_BASE = "http://192.168.2.36:15000"  # set your host:port
IDX_COMBINED = 182  # udevice expecting svalue="watt;day_kwh"
IDX_DAY: Optional[int] = 171  # set idx for daily kWh if desired
IDX_MONTH: Optional[int] = 175
IDX_LAST_MONTH: Optional[int] = 176
IDX_POWER_ONLY: Optional[int] = 172  # optional: live power only
DOMOTICZ_TIMEOUT = 5  # seconds

# ---------------------------------------------------------------------------


def _u16(hexdata: str, offset: int) -> int:
    return int(hexdata[offset * 2 : offset * 2 + 4], 16)


def _u32(hexdata: str, offset: int) -> int:
    return int(hexdata[offset * 2 : offset * 2 + 8], 16)


def parse_packet(hexdata: str) -> Dict[str, float]:
    """Decode a validated packet into human-friendly units."""
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

    watt_now = _u16(hexdata, inverter_now) * POWER_MULTIPLIER
    kwh_day = _u16(hexdata, inverter_day) / 100.0
    kwh_total = _u32(hexdata, inverter_tot) / 10.0
    temp = _u16(hexdata, inverter_temp) / 10.0
    dc_volts1 = _u16(hexdata, inverter_vdc1) / 10.0
    dc_volts2 = _u16(hexdata, inverter_vdc2) / 10.0
    dc_amps1 = _u16(hexdata, inverter_adc1) / 10.0
    dc_amps2 = _u16(hexdata, inverter_adc2) / 10.0
    ac_volts = _u16(hexdata, inverter_vac) / 10.0
    ac_amps = _u16(hexdata, inverter_aac) / 10.0
    ac_freq = _u16(hexdata, inverter_freq) / 100.0
    kwh_yesterday = _u16(hexdata, inverter_yes) / 100.0
    kwh_month = _u16(hexdata, inverter_mth)
    kwh_lastmonth = _u16(hexdata, inverter_lmth)

    return {
        "timestamp": time.strftime("%F %T"),
        "watt_now": watt_now,
        "kwh_day": kwh_day,
        "kwh_total": kwh_total,
        "dc_volts1": dc_volts1,
        "dc_volts2": dc_volts2,
        "dc_amps1": dc_amps1,
        "dc_amps2": dc_amps2,
        "ac_volts": ac_volts,
        "ac_amps": ac_amps,
        "ac_freq": ac_freq,
        "kwh_yesterday": kwh_yesterday,
        "kwh_month": kwh_month,
        "kwh_lastmonth": kwh_lastmonth,
        "temp": temp,
    }


def write_logs(data: Dict[str, float]) -> None:
    LOG_LATEST.write_text(json.dumps(data, indent=2))
    with LOG_HISTORY.open("a") as history:
        history.write(json.dumps(data, separators=(",", ":")) + "\n")


def _domoticz_get(params: Dict[str, str]) -> None:
    url = f"{DOMOTICZ_BASE}/json.htm?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=DOMOTICZ_TIMEOUT) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Domoticz responded with {resp.status}")


def push_to_domoticz(data: Dict[str, float]) -> None:
    if not DOMOTICZ_BASE:
        logging.debug("Domoticz disabled (DOMOTICZ_BASE empty)")
        return

    if IDX_COMBINED is not None:
        # Push live power and today's production (not lifetime total) in one device
        svalue = f"{int(data['watt_now'])};{data['kwh_day']}"
        _domoticz_get(
            {
                "type": "command",
                "param": "udevice",
                "idx": str(IDX_COMBINED),
                "nvalue": "0",
                "svalue": svalue,
            }
        )

    if IDX_POWER_ONLY is not None:
        _domoticz_get(
            {
                "type": "command",
                "param": "udevice",
                "idx": str(IDX_POWER_ONLY),
                "nvalue": "0",
                "svalue": str(int(data["watt_now"])),
            }
        )

    if IDX_DAY is not None:
        _domoticz_get(
            {
                "type": "command",
                "param": "udevice",
                "idx": str(IDX_DAY),
                "nvalue": "0",
                "svalue": str(data["kwh_day"]),
            }
        )

    if IDX_MONTH is not None:
        _domoticz_get(
            {
                "type": "command",
                "param": "udevice",
                "idx": str(IDX_MONTH),
                "nvalue": "0",
                "svalue": str(int(data["kwh_month"])),
            }
        )

    if IDX_LAST_MONTH is not None:
        _domoticz_get(
            {
                "type": "command",
                "param": "udevice",
                "idx": str(IDX_LAST_MONTH),
                "nvalue": "0",
                "svalue": str(int(data["kwh_lastmonth"])),
            }
        )


def handle_connection(rawdata: bytes) -> None:
    hexdata = binascii.hexlify(rawdata).decode()

    if not hexdata.startswith(HEADER_HEX):
        logging.warning("Invalid header: %s", hexdata[:8])
        return
    if len(hexdata) != EXPECTED_HEX_LEN:
        logging.warning("Unexpected packet length: %s", len(hexdata))
        return

    data = parse_packet(hexdata)
    write_logs(data)

    try:
        push_to_domoticz(data)
    except Exception as exc:  # noqa: BLE001
        logging.error("Domoticz push failed: %s", exc)
    else:
        logging.info(
            "Updated Domoticz: power=%s W total=%s kWh day=%s kWh",
            data["watt_now"],
            data["kwh_total"],
            data["kwh_day"],
        )


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        logging.info("Listening on %s:%s", HOST or "0.0.0.0", PORT)

        while True:
            sock.listen(1)
            conn, addr = sock.accept()
            with conn:
                rawdata = conn.recv(1024)
                if not rawdata:
                    continue
                logging.debug("Received %d bytes from %s", len(rawdata), addr)
                handle_connection(rawdata)


if __name__ == "__main__":
    main()
