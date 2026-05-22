import requests
import time
import hashlib
import os
from datetime import datetime

# ANSI Colors
G, Y, R, C, W, M, RS = "\033[92m", "\033[93m", "\033[91m", "\033[96m", "\033[97m", "\033[95m", "\033[0m"

class XophyWatchtower:
    def __init__(self, target, interval=60):
        self.target = f"https://{target}" if not target.startswith('http') else target
        self.domain = self.target.split('//')[-1].split('/')[0]
        self.interval = interval 
        self.last_hash = None
        self.headers = {"User-Agent": "XOPHY-Watchtower/4.0 (Security Research)"}

    def trigger_alert(self, msg):
        """Triggers a system beep and a desktop notification."""
        # 1. Terminal Beep (ASCII Bell)
        print("\a", end="") 
        
        # 2. Desktop Notification (Works on Kali/Linux)
        try:
            # Using notify-send (Standard on Kali)
            title = "XOPHY WATCHTOWER ALERT"
            cmd = f'notify-send "{title}" "{msg}" --icon=dialog-warning'
            os.system(cmd)
        except Exception:
            pass

    def get_site_hash(self):
        """Creates a SHA-256 fingerprint of the target's current state."""
        try:
            res = requests.get(self.target, headers=self.headers, timeout=10, verify=False)
            if res.status_code == 200:
                return hashlib.sha256(res.text.encode('utf-8')).hexdigest()
        except:
            return None
        return None

    def run(self):
        print(f"\n  {M}╔════════════════════════════════════════════════════════════════╗{RS}")
        print(f"  {M}║                XOPHY WATCHTOWER (LIVE MONITOR)                 ║{RS}")
        print(f"  {M}╚════════════════════════════════════════════════════════════════╝{RS}")
        print(f"  {C}[*] Monitoring Target : {W}{self.target}{RS}")
        print(f"  {C}[*] Status            : {G}ACTIVE{RS}")
        print(f"  {Y}[!] Alerts Enabled    : Desktop Notification + Audio{RS}\n")

        try:
            while True:
                current_time = datetime.now().strftime("%H:%M:%S")
                current_hash = self.get_site_hash()

                if current_hash is None:
                    print(f"  [{current_time}] {R}✖ Target unreachable. Retrying...{RS}")
                elif self.last_hash is None:
                    print(f"  [{current_time}] {G}● Initializing Baseline for {self.domain}...{RS}")
                    self.last_hash = current_hash
                elif current_hash != self.last_hash:
                    alert_msg = f"Change detected on {self.domain}!"
                    print(f"\n  [{current_time}] {R}⚡ ALERT: CHANGE DETECTED!{RS}")
                    
                    self.trigger_alert(alert_msg)
                    
                    print(f"  {Y}[!] The target's source code has been modified.{RS}")
                    self.last_hash = current_hash
                else:
                    # Rolling update in terminal
                    print(f"  [{current_time}] {C}◌ Monitoring {self.domain}... No changes.{RS}", end="\r")

                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f"\n\n  {W}[*] Watchtower standing down...{RS}")

def run(target):
    # Default interval of 60 seconds
    watcher = XophyWatchtower(target, interval=60)
    watcher.run()
