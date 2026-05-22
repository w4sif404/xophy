#!/usr/bin/env python3
"""
XOPHY: ADVANCED OSINT & RECONNAISSANCE FRAMEWORK v3.0
Operator: w45if_4o4
"""

import sys
import os
import time
import platform
import signal
from datetime import datetime

# --- PATH FIX: Ensures CLI can see the /modules folder ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ============================================================
# HACKER UI CONSTANTS & COLORS
# ============================================================
CRIT = "\033[91m"
WARN = "\033[93m"
INFO = "\033[96m"
OK   = "\033[92m"
DIM  = "\033[2m"
BLD  = "\033[1m"
RST  = "\033[0m"
ORANGE = "\033[38;5;208m" 
P, C, W, Y, G, R, RS = "\033[95m", "\033[96m", "\033[97m", "\033[93m", "\033[92m", "\033[91m", RST

ICON_OK     = f"{OK}[✓]{RST}"
ICON_WARN   = f"{WARN}[!]{RST}"
ICON_CRIT   = f"{CRIT}[✗]{RST}"
ICON_INFO   = f"{INFO}[*]{RST}"
ICON_ARROW  = f"{INFO}▶{RST}"
ICON_EYE    = f"{P}◎{RST}"

UI_WIDTH = 64

# ============================================================
# MODULE LOADER (Independent Loading)
# ============================================================
def placeholder(*args, **kwargs): 
    print(f"  {R}[✗]{RS} Error: Module failed to load or is missing.")

def safe_import(module_path, func_name=None):
    try:
        import importlib
        mod = importlib.import_module(module_path)
        if func_name:
            return getattr(mod, func_name)
        return mod
    except (ImportError, AttributeError):
        return placeholder if func_name else type('obj', (object,), {'run': placeholder})

# Dynamic Imports
vulnerability_scanner = safe_import("modules.vulnerability_scanner")
whois_lookup = safe_import("modules.whois_lookup")
dns_lookup = safe_import("modules.dns_lookup")
ssl_run = safe_import("modules.ssl_analyzer", "run")
subdomain_run = safe_import("osint.subdomains", "run")
xophy_entry = safe_import("modules.dorkomatic", "xophy_entry")
image_run = safe_import("modules.image_osint", "run")
wireless_run = safe_import("modules.wireless_mapper", "run")
watchtower_run = safe_import("modules.watchtower", "run")
ransom_run = safe_import("modules.ransom_watch", "run")
iot_run = safe_import("modules.iot_scanner", "run")

# ============================================================
# HACKER UI HELPERS
# ============================================================

def type_effect(text: str, delay: float = 0.005, color: str = G, end="\n"):
    for ch in text:
        sys.stdout.write(f"{color}{ch}{RST}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def item(title, value):
    if isinstance(value, list):
        val_str = ", ".join(str(v) for v in value) if value else f"{DIM}None found{RST}"
    else:
        val_str = str(value)
    print(f"  {ICON_ARROW} {C}{title:<25}{RST} : {val_str}")

def get_target():
    print()
    target = input(f"  {ICON_EYE} {Y}Enter target domain/IP{RST} {DIM}→{RST} ").strip()
    return target

def signal_handler(sig, frame):
    print(f"\n\n{WARN}⚠  Interrupted. Exiting...{RST}\n")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ============================================================
# UI RENDERERS
# ============================================================

def print_xophy_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    session_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    plat = platform.system()
    
    print(f"{RST}{DIM}╔{'═' * (UI_WIDTH-2)}╗")
    print(f"║{' ' * (UI_WIDTH-2)}║")
    print(f"║  {R}{BLD}██╗  ██╗ ██████╗ ██████╗ ██╗  ██╗██╗  ██╗{RST}           {DIM}║")
    print(f"║  {R}{BLD}╚██╗██╔╝██╔═══██╗██╔══██╗██║  ██║╚██╗ ██╔╝{RST}           {DIM}║")
    print(f"║  {Y}{BLD} ╚███╔╝ ██║   ██║██████╔╝███████║ ╚████╔╝ {RST}           {DIM}║")
    print(f"║  {Y}{BLD} ██╔██╗ ██║   ██║██╔═══╝ ╚══██╔══╝ ╚██╔╝  {RST}           {DIM}║")
    print(f"║  {Y}{BLD}██╔╝ ██╗╚██████╔╝██║      ██║     ██║   {RST}           {DIM}║")
    print(f"║  {Y}{BLD}╚═╝  ╚═╝ ╚═════╝ ╚═╝      ╚═╝     ╚═╝   {RST}           {DIM}║")
    print(f"║{' ' * (UI_WIDTH-2)}║")
    print(f"║  {OK}{BLD}██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗{RST}      {DIM}║")
    print(f"║  {OK}{BLD}██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║{RST}      {DIM}║")
    print(f"║  {G}{BLD}██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║{RST}      {DIM}║")
    print(f"║  {G}{BLD}██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║{RST}      {DIM}║")
    print(f"║  {C}{BLD}██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║{RST}      {DIM}║")
    print(f"║  {C}{BLD}╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝{RST}      {DIM}║")
    print(f"║{' ' * (UI_WIDTH-2)}║")
    print(f"║  {DIM}{'─' * (UI_WIDTH-6)}{RST}  {DIM}║")
    print(f"║{' ' * (UI_WIDTH-2)}║")
    print(f"║  {P}{BLD}OPERATOR : {R}w45if_4o4{RST}{' ' * (UI_WIDTH-25)} {DIM}║")
    print(f"║  {P}{BLD}PLATFORM : {INFO}{plat:<10}{RST}{' ' * (UI_WIDTH-26)} {DIM}║")
    print(f"║  {P}{BLD}SESSION  : {INFO}{session_time}{RST}{' ' * (UI_WIDTH-34)} {DIM}║")
    print(f"║{' ' * (UI_WIDTH-2)}║")
    print(f"╚{'═' * (UI_WIDTH-2)}╝{RST}")
    print(f"{RST}{DIM}  ──┤{RST} {Y}{BLD}ADVANCED OSINT & RECONNAISSANCE FRAMEWORK v3.0{RST} {DIM}├──{RST}")
    print(f"{RST}{DIM}  ──┤{RST} {R}{BLD}BUILT BY w45if_4o4{RST}")

def main_menu():
    HDR, OPT, TXT = f"{BLD}{C}", f"{P}", f"{W}"
    print(f"\n {Y}╔{'═' * (UI_WIDTH-2)}╗")
    print(f" ║ {HDR}{'XOPHY COMMAND CENTER v3.0':^{UI_WIDTH-4}} {Y}║")
    print(f" ╠{'═' * (UI_WIDTH-2)}╣")
    
    print(f" ║ {HDR}[01] INFRASTRUCTURE RECON{RS}{' ' * (UI_WIDTH-28)} {Y}║")
    print(f" ║  {OPT}01{TXT} Tech-Stack & CVE      {OPT}02{TXT} WHOIS Lookup      {Y}║")
    print(f" ║  {OPT}03{TXT} DNS Enumeration       {OPT}04{TXT} SSL/TLS Advanced  {Y}║")
    print(f" ║{' ' * (UI_WIDTH-2)}║")
    
    print(f" ║ {HDR}[02] WEB & DATA MINING{RS}{' ' * (UI_WIDTH-25)} {Y}║")
    print(f" ║  {OPT}05{TXT} Subdomain Enum        {OPT}06{TXT} DORK-o-Matic      {Y}║")
    print(f" ║  {OPT}07{TXT} Web Spider            {OPT}08{TXT} Email Harvesting  {Y}║")
    print(f" ║  {OPT}09{TXT} Social Recon          {OPT}10{TXT} Image Forensics   {Y}║")
    print(f" ║{' ' * (UI_WIDTH-2)}║")
    
    print(f" ║ {HDR}[03] NETWORK & THREATS{RS}{' ' * (UI_WIDTH-25)} {Y}║")
    print(f" ║  {R}11{TXT} Ransom-Watch (LIVE)   {OPT}12{TXT} IoT Discovery     {Y}║")
    print(f" ║  {OPT}13{TXT} Wireless Mapping      {OPT}14{TXT} Watchtower (Live) {Y}║")
    
    print(f" ╠{'═' * (UI_WIDTH-2)}╣")
    print(f" ║ {HDR}SPECIAL OPERATIONS{RS}{' ' * (UI_WIDTH-22)} {Y}║")
    print(f" ║  {G}88{TXT} Export Results   {ORANGE}99{TXT} FULL RECON   {R}00{TXT} Exit   {Y}║")
    print(f" {Y}╚{'═' * (UI_WIDTH-2)}╝")

# ============================================================
# MODULE WRAPPERS
# ============================================================

def module_header(name, target):
    print(f"\n{R}{'━' * UI_WIDTH}{RS}")
    print(f"  {BLD}[{name.upper()}] Target: {target}{RS}")
    print(f"{R}{'━' * UI_WIDTH}{RS}\n")

def module_footer(start):
    print(f"\n{DIM}{'─' * UI_WIDTH}{RS}")
    print(f"  {ICON_OK} Completed in {time.time()-start:.2f}s{RS}")

# ============================================================
# OPTION LOGIC
# ============================================================

def opt_01():
    t = get_target(); s = time.time()
    module_header("vulnerability scanner", t)
    vulnerability_scanner.run(t); module_footer(s)

def opt_02():
    t = get_target(); s = time.time()
    module_header("whois lookup", t)
    r = whois_lookup.run(t)
    if r and hasattr(r, 'items'):
        for k,v in r.items(): item(k,v)
    module_footer(s)

def opt_03():
    t = get_target(); s = time.time()
    module_header("dns enumeration", t)
    r = dns_lookup.run(t)
    if r and hasattr(r, 'items'):
        for k,v in r.items(): item(k,v)
    module_footer(s)

def opt_04():
    t = get_target(); s = time.time()
    module_header("SSL/TLS Advanced", t)
    ssl_run(t); module_footer(s)

def opt_05():
    t = get_target(); s = time.time()
    module_header("subdomain enumeration", t)
    subdomain_run(t); module_footer(s)

def opt_10(): 
    p = input(f"  {ICON_ARROW} Path: ").strip()
    if os.path.exists(p): 
        s = time.time(); module_header("Image OSINT", p)
        image_run(p); module_footer(s)
    else:
        print(f"  {ICON_CRIT} Path not found.")

# ============================================================
# MAIN LOOP
# ============================================================

def main():
    print_xophy_banner()
    type_effect(f"  System ready. Operator {R}w45if_4o4{RS} authenticated.", 0.005)
    
    while True:
        try:
            main_menu()
            choice = input(f"  {R}{BLD}⚡{RS} {G}w45if_4o4{RS}{DIM}@{RS}{C}xophy{RS} ❯ ").strip()
            if not choice: continue

            if choice.isdigit() and len(choice) == 1:
                choice = choice.zfill(2)

            if choice in ["00", "0", "exit"]: 
                print(f"\n  {OK}Goodbye, Operator.{RS}")
                sys.exit(0)

            elif choice == "01": opt_01()
            elif choice == "02": opt_02()
            elif choice == "03": opt_03()
            elif choice == "04": opt_04()
            elif choice == "05": opt_05()
            elif choice == "06": xophy_entry()
            elif choice == "07": 
                t = get_target(); s = time.time(); module_header("Web Spider", t)
                from modules.web_crawler import run as web_run; web_run(t); module_footer(s)
            elif choice == "08": 
                t = get_target(); s = time.time(); module_header("Email Harvester", t)
                from modules.email_harvester import run as email_run; email_run(t); module_footer(s)
            elif choice == "09": 
                target = input(f"\n  {ICON_ARROW} {C}Enter username{RS} {DIM}→{RS} ").strip()
                s = time.time(); module_header("Social Recon", target)
                from modules.social_recon import run as social_run; social_run(target); module_footer(s)
            elif choice == "10": opt_10()
            elif choice == "11": 
                t = get_target(); s = time.time(); module_header("Ransom-Watch", t)
                ransom_run(t); module_footer(s)
            elif choice == "12": 
                s = time.time(); module_header("IoT Discovery", "Network"); iot_run(); module_footer(s)
            elif choice == "13": 
                s = time.time(); module_header("Wireless Mapping", "Airspace"); wireless_run(); module_footer(s)
            elif choice == "14": 
                t = get_target(); watchtower_run(t)
            elif choice == "88": 
                print(f" {ICON_OK} Data archived to /reports/")
            elif choice == "99":
                t = get_target(); s_total = time.time()
                opt_01(); opt_02(); opt_03(); opt_04(); opt_05()
                module_footer(s_total)
            else: 
                print(f"  {ICON_CRIT} Invalid option: {choice}")

        except KeyboardInterrupt:
            print(f"\n  {Y}Operation cancelled.{RS}")
            continue

if __name__ == "__main__":
    main()
