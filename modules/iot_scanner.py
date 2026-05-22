#!/usr/bin/env python3
"""
ADVANCED IOT DISCOVERY v4.0 - OPTIMIZED
Author: w45if_4o4
Features: Fast scanning, subnet limiting, intelligent discovery
"""

import socket
import subprocess
import ipaddress
import threading
import time
import re
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================== COLORS ==================
OK   = "\033[92m"
WARN = "\033[93m"
CRIT = "\033[91m"
INFO = "\033[96m"
DIM  = "\033[2m"
RST  = "\033[0m"
CYAN = "\033[36m"
MAG  = "\033[35m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
BOLD = "\033[1m"

# ================== OPTIMIZED VENDOR DB ==================
VENDOR_DB = {
    "080027": {"name": "VirtualBox", "type": "Virtual Machine", "risk": "LOW"},
    "52550A": {"name": "VirtualBox", "type": "Virtual Machine", "risk": "LOW"},
    "000C29": {"name": "VMware", "type": "Virtual Machine", "risk": "LOW"},
    "B827EB": {"name": "Raspberry Pi", "type": "SBC", "risk": "MEDIUM"},
    "F0D5BF": {"name": "Hikvision", "type": "IP Camera", "risk": "HIGH"},
    "ACCC8E": {"name": "TP-Link", "type": "Network", "risk": "MEDIUM"},
    "28AD3E": {"name": "Xiaomi", "type": "IoT", "risk": "MEDIUM"},
    "FC3497": {"name": "Ubiquiti", "type": "Network", "risk": "MEDIUM"},
    "00:16:6C": {"name": "Asustor", "type": "NAS", "risk": "HIGH"},
    "00:11:32": {"name": "Synology", "type": "NAS", "risk": "HIGH"},
    "00:0E:08": {"name": "Cisco", "type": "Network", "risk": "HIGH"},
}

# ================== OPTIMIZED PORT SCAN ==================
FAST_PORTS = [22, 23, 80, 443, 445, 554, 1883, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]

PORT_DB = {
    22: {"name": "SSH", "risk": "MEDIUM"},
    23: {"name": "Telnet", "risk": "CRITICAL"},
    80: {"name": "HTTP", "risk": "MEDIUM"},
    443: {"name": "HTTPS", "risk": "LOW"},
    445: {"name": "SMB", "risk": "CRITICAL"},
    554: {"name": "RTSP", "risk": "HIGH"},
    1883: {"name": "MQTT", "risk": "CRITICAL"},
    3306: {"name": "MySQL", "risk": "HIGH"},
    3389: {"name": "RDP", "risk": "CRITICAL"},
    5432: {"name": "PostgreSQL", "risk": "HIGH"},
    5900: {"name": "VNC", "risk": "CRITICAL"},
    6379: {"name": "Redis", "risk": "HIGH"},
    8080: {"name": "HTTP-Alt", "risk": "MEDIUM"},
    8443: {"name": "HTTPS-Alt", "risk": "LOW"},
    27017: {"name": "MongoDB", "risk": "CRITICAL"},
}

# ================== OPTIMIZED FUNCTIONS ==================

def get_local_subnets():
    """Get local subnets (limited to /24 for speed)"""
    subnets = []
    
    try:
        # Get default gateway interface
        result = subprocess.run(["ip", "route", "show", "default"], 
                               capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            match = re.search(r'dev\s+(\w+)', line)
            if match:
                iface = match.group(1)
                # Get IP for this interface
                ip_result = subprocess.run(["ip", "-4", "addr", "show", iface],
                                          capture_output=True, text=True)
                for ip_line in ip_result.stdout.split('\n'):
                    ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)/(\d+)', ip_line)
                    if ip_match:
                        ip = ip_match.group(1)
                        mask = int(ip_match.group(2))
                        # Only use /24 subnets for speed
                        if mask <= 24:
                            network = str(ipaddress.ip_network(f"{ip}/{mask}", strict=False))
                            subnets.append(network)
                        else:
                            # For smaller masks, convert to /24
                            base = '.'.join(ip.split('.')[:3])
                            subnets.append(f"{base}.0/24")
    except:
        pass
    
    # Fallback to /24 on common subnets
    if not subnets:
        subnets = ["192.168.1.0/24", "10.0.0.0/24", "172.16.0.0/24"]
    
    # Remove duplicates and limit to 3 subnets
    subnets = list(set(subnets))[:3]
    
    return subnets

def fast_ping(ip):
    """Ultra-fast host discovery using ARP only"""
    try:
        # ARP ping is fastest for local networks
        result = subprocess.run(["arping", "-c", "1", "-w", "1", ip],
                               capture_output=True, timeout=2)
        if result.returncode == 0:
            return True
    except:
        pass
    
    # Fallback to TCP quick check
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        for port in [80, 443, 22]:
            if sock.connect_ex((ip, port)) == 0:
                sock.close()
                return True
        sock.close()
    except:
        pass
    
    return False

def get_mac_vendor_fast(ip):
    """Fast MAC and vendor lookup"""
    try:
        result = subprocess.run(["ip", "neigh", "show", ip],
                               capture_output=True, text=True, timeout=2)
        mac_match = re.search(r"lladdr\s(([0-9a-f]{2}:){5}[0-9a-f]{2})", result.stdout, re.I)
        
        if mac_match:
            mac = mac_match.group(1)
            oui = mac.replace(":", "").upper()[:6]
            
            if oui in VENDOR_DB:
                v = VENDOR_DB[oui]
                return mac, v["name"], v["type"], v["risk"]
            return mac, "Unknown Device", "Generic", "MEDIUM"
    except:
        pass
    
    return "Unknown", "Unknown Device", "Generic", "MEDIUM"

def fast_port_scan(ip):
    """Quick port scan on critical ports only"""
    open_ports = []
    
    for port in FAST_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            if sock.connect_ex((ip, port)) == 0:
                port_info = PORT_DB.get(port, {"name": "Unknown", "risk": "MEDIUM"})
                open_ports.append({
                    "port": port,
                    "name": port_info["name"],
                    "risk": port_info["risk"]
                })
            sock.close()
        except:
            pass
    
    return open_ports

def calculate_risk_fast(ports, vendor_risk):
    """Quick risk calculation"""
    score = 0
    
    if vendor_risk == "CRITICAL":
        score += 40
    elif vendor_risk == "HIGH":
        score += 30
    elif vendor_risk == "MEDIUM":
        score += 15
    
    for port in ports:
        if port["risk"] == "CRITICAL":
            score += 25
        elif port["risk"] == "HIGH":
            score += 15
        elif port["risk"] == "MEDIUM":
            score += 5
    
    if score >= 70:
        return "CRITICAL", f"{CRIT}🔥 CRITICAL{RST}"
    elif score >= 40:
        return "HIGH", f"{CRIT}⚠️ HIGH{RST}"
    elif score >= 20:
        return "MEDIUM", f"{WARN}⚠️ MEDIUM{RST}"
    else:
        return "LOW", f"{OK}✅ LOW{RST}"

# ================== MAIN RUN ==================

def run(_=None):
    operator = "w45if_4o4"
    start = time.time()
    
    print(f"\n{MAG}{'━'*60}{RST}")
    print(f"{MAG}{BOLD}  ⚡ ADVANCED IOT DISCOVERY v4.0 (FAST){RST}")
    print(f"  {INFO}Operator: {CRIT}{operator}{RST}")
    print(f"  {INFO}Started : {datetime.now().strftime('%H:%M:%S')}{RST}")
    print(f"{MAG}{'━'*60}{RST}\n")
    
    # Get local subnets
    subnets = get_local_subnets()
    
    print(f"  {INFO}[*] Detected subnets: {', '.join(subnets)}{RST}\n")
    
    all_devices = []
    total_hosts = 0
    
    for subnet in subnets:
        net = ipaddress.ip_network(subnet)
        total_hosts += net.num_addresses
        
        # Show progress estimate
        print(f"  {INFO}[*] Scanning {subnet} ({net.num_addresses} IPs)...{RST}")
        print(f"  {DIM}    This will take ~{net.num_addresses // 100} seconds{RST}\n")
        
        alive_hosts = []
        ips = list(net.hosts())[:254]  # Limit to 254 IPs for speed
        
        # Parallel ping with progress
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(fast_ping, str(ip)): str(ip) for ip in ips}
            
            completed = 0
            for future in as_completed(futures):
                ip = futures[future]
                completed += 1
                
                if completed % 50 == 0:
                    print(f"  {DIM}    Progress: {completed}/{len(ips)} IPs scanned{RST}", end="\r")
                
                if future.result():
                    alive_hosts.append(ip)
                    print(f"\n  {OK}[+]{RST} Found: {CYAN}{ip}{RST}")
        
        print(f"\n  {OK}[✓] Found {len(alive_hosts)} active devices in {subnet}{RST}\n")
        
        # Scan each alive host
        for idx, ip in enumerate(sorted(alive_hosts), 1):
            # Get MAC and vendor
            mac, vendor, device_type, vendor_risk = get_mac_vendor_fast(ip)
            
            # Fast port scan
            open_ports = fast_port_scan(ip)
            
            # Calculate risk
            risk_level, risk_display = calculate_risk_fast(open_ports, vendor_risk)
            
            # Display results
            print(f"  {DIM}┌─ Device #{idx:02} {'─'*40}{RST}")
            print(f"  {DIM}│{RST} {CYAN}IP{RST}      : {ip}")
            print(f"  {DIM}│{RST} {INFO}MAC{RST}     : {mac}")
            print(f"  {DIM}│{RST} {INFO}Vendor{RST}  : {vendor}")
            print(f"  {DIM}│{RST} {INFO}Type{RST}    : {device_type}")
            print(f"  {DIM}│{RST} {INFO}Risk{RST}    : {risk_display}")
            
            if open_ports:
                port_list = [f"{p['port']}/{p['name']}" for p in open_ports]
                print(f"  {DIM}│{RST} {INFO}Ports{RST}   : {', '.join(port_list)}")
                
                # Show critical ports
                critical_ports = [p for p in open_ports if p["risk"] == "CRITICAL"]
                if critical_ports:
                    print(f"  {DIM}│{RST} {CRIT}⚠️  Critical: {', '.join([str(p['port']) for p in critical_ports])}{RST}")
            
            print(f"  {DIM}└{'─'*52}{RST}\n")
            
            all_devices.append({
                "ip": ip,
                "mac": mac,
                "vendor": vendor,
                "device_type": device_type,
                "risk_level": risk_level,
                "ports": open_ports
            })
    
    # Summary
    elapsed = time.time() - start
    critical_count = sum(1 for d in all_devices if d["risk_level"] == "CRITICAL")
    high_count = sum(1 for d in all_devices if d["risk_level"] == "HIGH")
    
    print(f"  {BOLD}{INFO}📊 SCAN SUMMARY{RST}")
    print(f"  {DIM}{'─'*60}{RST}")
    print(f"  {INFO}Time elapsed : {elapsed:.2f} seconds")
    print(f"  {INFO}Total devices : {len(all_devices)}")
    print(f"  {CRIT}Critical risk : {critical_count}{RST}")
    print(f"  {CRIT}High risk     : {high_count}{RST}")
    
    # Save report
    if all_devices:
        os.makedirs("reports", exist_ok=True)
        report_file = f"reports/iot_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(all_devices, f, indent=2)
        print(f"  {INFO}Report saved  : {report_file}{RST}")
    
    if critical_count > 0:
        print(f"\n  {CRIT}{BOLD}🔥 IMMEDIATE ACTION REQUIRED!{RST}")
        print(f"  {CRIT}  {critical_count} CRITICAL risk devices found!{RST}")
    
    print(f"\n{DIM}{'─'*60}{RST}")
    print(f"  {OK}[✓] Module completed in {elapsed:.2f}s | operator: {operator}{RST}")
    print(f"{DIM}{'─'*60}{RST}\n")
    
    return all_devices

if __name__ == "__main__":
    run()
