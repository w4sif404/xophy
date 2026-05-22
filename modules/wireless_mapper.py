#!/usr/bin/env python3

import subprocess
import time
import os
import re
import shutil
from datetime import datetime

# ================= COLORS =================
OK   = "\033[92m"
WARN = "\033[93m"
CRIT = "\033[91m"
INFO = "\033[96m"
DIM  = "\033[2m"
RST  = "\033[0m"
CYAN = "\033[36m"
MAG  = "\033[35m"

# ================= UTILS =================

def tool_exists(tool):
    return shutil.which(tool) is not None

def require_tools():
    required = ["iw", "airodump-ng", "bluetoothctl"]
    missing = [t for t in required if not tool_exists(t)]
    if missing:
        print(f"{CRIT}[✗] Missing tools: {', '.join(missing)}{RST}")
        print(f"{WARN}    Install: aircrack-ng, bluez, iw{RST}")
        return False
    return True

def get_wireless_interfaces():
    out = subprocess.check_output(["iw", "dev"], stderr=subprocess.DEVNULL).decode()
    return re.findall(r"Interface\s+(\w+)", out)

def enable_monitor_mode(iface):
    subprocess.run(["ip", "link", "set", iface, "down"], stdout=subprocess.DEVNULL)
    subprocess.run(["iw", iface, "set", "monitor", "control"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", iface, "up"], stdout=subprocess.DEVNULL)

# ================= WIFI SCAN =================

def scan_wifi(iface, duration=12):
    print(f"{INFO}[*] Scanning Wi-Fi networks ({duration}s)...{RST}")
    csv = "/tmp/xophy_wifi"

    proc = subprocess.Popen(
        ["airodump-ng", iface, "--output-format", "csv", "-w", csv],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(duration)
    proc.terminate()

    return parse_airodump(csv + "-01.csv")

def parse_airodump(csv_file):
    networks = []
    if not os.path.exists(csv_file):
        return networks

    with open(csv_file, errors="ignore") as f:
        for line in f:
            if "Station MAC" in line:
                break
            fields = line.split(",")
            if len(fields) > 13 and fields[0].strip():
                bssid = fields[0].strip()
                pwr = fields[8].strip()
                ch  = fields[3].strip()
                enc = fields[5].strip()
                ssid = fields[13].strip()

                risk = f"{OK}LOW{RST}"
                if "WEP" in enc or "OPN" in enc:
                    risk = f"{CRIT}HIGH{RST}"
                elif "WPA" in enc:
                    risk = f"{WARN}MEDIUM{RST}"

                networks.append({
                    "ssid": ssid or "<Hidden>",
                    "bssid": bssid,
                    "channel": ch,
                    "signal": pwr,
                    "encryption": enc,
                    "risk": risk
                })
    return networks

# ================= BLUETOOTH =================

def scan_bluetooth(duration=8):
    print(f"{INFO}[*] Scanning Bluetooth devices ({duration}s)...{RST}")
    devices = []

    proc = subprocess.Popen(
        ["bluetoothctl", "scan", "on"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    start = time.time()
    while time.time() - start < duration:
        line = proc.stdout.readline()
        if "Device" in line:
            parts = line.split()
            if len(parts) >= 3:
                devices.append({
                    "mac": parts[2],
                    "name": " ".join(parts[3:])
                })

    subprocess.run(["bluetoothctl", "scan", "off"], stdout=subprocess.DEVNULL)
    return devices

# ================= MAIN =================

def run(_=None):
    operator = "w45if_4o4"

    print(f"\n{MAG}{'━'*68}{RST}")
    print(f"{MAG}  [WIRELESS NETWORK MAPPING]{RST}")
    print(f"  ◎ Target   : {CYAN}PHYSICAL AIRSPACE{RST}")
    print(f"  ◎ Operator : {CYAN}{operator}{RST}")
    print(f"  ◎ Started  : {CYAN}{datetime.now().strftime('%H:%M:%S')}{RST}")
    print(f"{MAG}{'━'*68}{RST}\n")

    if not require_tools():
        return

    ifaces = get_wireless_interfaces()
    if not ifaces:
        print(f"{CRIT}[✗] No wireless interfaces found{RST}")
        return

    iface = ifaces[0]
    print(f"{OK}[✓] Using interface: {iface}{RST}")
    enable_monitor_mode(iface)

    wifi_networks = scan_wifi(iface)
    bt_devices = scan_bluetooth()

    # ================= OUTPUT =================

    print(f"\n{OK}[✓] Wi-Fi Networks Found: {len(wifi_networks)}\n")
    for i, net in enumerate(wifi_networks, 1):
        print(f"  {DIM}┌─ AP #{i:02} {'─'*42}{RST}")
        print(f"  {DIM}│{RST} SSID       : {CYAN}{net['ssid']}{RST}")
        print(f"  {DIM}│{RST} BSSID      : {net['bssid']}")
        print(f"  {DIM}│{RST} Channel    : {net['channel']}")
        print(f"  {DIM}│{RST} Signal     : {net['signal']}")
        print(f"  {DIM}│{RST} Encryption : {net['encryption']}")
        print(f"  {DIM}│{RST} Risk       : {net['risk']}")
        print(f"  {DIM}└{'─'*56}{RST}\n")

    print(f"{OK}[✓] Bluetooth Devices Found: {len(bt_devices)}\n")
    for i, d in enumerate(bt_devices, 1):
        print(f"  {DIM}┌─ BT Device #{i:02} {'─'*38}{RST}")
        print(f"  {DIM}│{RST} MAC  : {d['mac']}")
        print(f"  {DIM}│{RST} Name : {d['name']}")
        print(f"  {DIM}└{'─'*56}{RST}\n")

    print(f"{DIM}{'─'*68}{RST}")
    print(f"  {OK}[✓] Module completed | operator: {operator}")
    print(f"{DIM}{'─'*68}{RST}")
