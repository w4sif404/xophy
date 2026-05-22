import time
import sys
import threading
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ANSI Colors
G, R, Y, C, W, DIM, RS = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[97m', '\033[2m', '\033[0m'

class RansomWatchPro:
    def __init__(self, target):
        self.target = target
        self.operator = "w45if_4o4"
        # API Key placeholder - Ensure yours is active at otx.alienvault.com
        self.OTX_KEY = "a3b99064da106fc290ea79384a001809ac9c7337f60460be0db3b6e08ba7bb67" 
        self.results = {"otx": []}
        self.error_occurred = False

    def banner(self):
        print(f"\n {G}⚡ {self.operator}@xophy ❯ Ransom-Watch v3.0{RS}")
        print(f" {W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}")
        print(f" {C}[THREAT INTEL ENGINE]{RS}")
        print(f" {W}◎ Target   : {Y}{self.target}{RS}")
        print(f" {W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RS}\n")

    def fetch_otx(self):
        """Advanced fetch with persistent session and auto-retry logic"""
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{self.target}/general"
        headers = {
            "X-OTX-API-KEY": self.OTX_KEY,
            "User-Agent": "XOPHY-Framework/v3.0"
        }
        
        # Setup session with retry strategy for high reliability
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
        try:
            # 15s timeout to handle heavy API loads
            response = session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                self.results["otx"] = data.get('pulse_info', {}).get('pulses', [])
            else:
                self.error_occurred = True
                print(f" {R}[!] Node Error: HTTP {response.status_code}{RS}")
                
        except requests.exceptions.Timeout:
            self.error_occurred = True
            print(f" {R}[!] Connection Timeout: AlienVault Nodes are unresponsive.{RS}")
        except Exception as e:
            self.error_occurred = True
            print(f" {R}[!] Critical Failure: {str(e)}{RS}")

    def run_scan(self):
        self.banner()
        
        # Professional Threaded Loader
        thread = threading.Thread(target=self.fetch_otx)
        thread.start()
        
        while thread.is_alive():
            for char in ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]:
                sys.stdout.write(f"\r {W}[*] Synchronizing Intelligence Nodes {C}{char}{RS}")
                sys.stdout.flush()
                time.sleep(0.08)
        
        print(f"\r {G}[+] Intelligence Retrieval Complete.                      {RS}\n")

        if self.error_occurred:
            print(f" {Y}[!] Warning: Intelligence report is incomplete due to network lag.{RS}")
            return

        pulses = self.results["otx"]
        if pulses:
            count = len(pulses)
            level = f"{R}CRITICAL" if count > 8 else f"{Y}MODERATE"
            
            print(f" {R}[!!!] ALERT: {count} ACTIVE THREAT PULSES IDENTIFIED [!!!]{RS}")
            print(f" {W}Intelligence Confidence: {G}HIGH{RS} | Severity: {level}{RS}\n")

            # Deep Analysis of Top Pulses
            for p in pulses[:5]:
                name = p.get('name', 'Unknown Threat Actor/Campaign')
                author = p.get('author_name', 'Anonymous Intel')
                created = p.get('created', '0000-00-00')[:10]
                tags = p.get('tags', [])
                
                # Parsing specific indicators
                tag_display = f"{C}" + ", ".join(tags[:3]) + f"{RS}" if tags else f"{DIM}Generic Threat{RS}"

                print(f" {W}» {Y}Campaign:{RS} {name}")
                print(f"   {C}└─ Date:{RS} {created} | {C}Author:{RS} {author}")
                print(f"   {R}└─ Intel Tags:{RS} {tag_display}")
                print(f"   {DIM}{'─' * 45}{RS}")

            # Intelligent Recommendation Logic
            print(f"\n {C}[THREAT ANALYSIS]{RS}")
            if any("ransomware" in str(t).lower() for t in pulses):
                print(f" {R}[!] HIGH RISK: Specific ransomware patterns detected in history.{RS}")
            
            print(f" {Y}[RECO] Action: Block associated IPs and monitor for unusual outbound traffic.{RS}")
        else:
            print(f" {G}[INFO] Reputation Check: Target appears clean in current AlienVault OTX pulses.{RS}")

def run(target):
    # Sanitize input: remove protocol and trailing paths
    clean_target = target.replace("https://", "").replace("http://", "").split('/')[0]
    scanner = RansomWatchPro(clean_target)
    scanner.run_scan()

if __name__ == "__main__":
    try:
        t = input(f" {C}◎ Enter Target Domain → {RS}").strip()
        if t: 
            run(t)
        else:
            print(f" {R}[!] Error: No target provided.{RS}")
    except KeyboardInterrupt:
        print(f"\n\n {R}[!] Module Shutdown by Operator.{RS}")
        sys.exit(0)
