import requests
import re
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# ANSI Colors
G, Y, R, C, W, M, RS = "\033[92m", "\033[93m", "\033[91m", "\033[96m", "\033[97m", "\033[95m", "\033[0m"

class XophyHarvester:
    def __init__(self, target):
        self.target = f"https://{target}" if not target.startswith('http') else target
        self.domain = urlparse(self.target).netloc
        self.emails = set()
        self.headers = {'User-Agent': 'Xophy-Bot/4.0 (Educational Security Research)'}

    def scrape_page(self, url):
        """Extracts emails directly from a specific page's HTML."""
        try:
            response = requests.get(url, headers=self.headers, timeout=5, verify=False)
            if response.status_code == 200:
                # Regex looks for standard email patterns ending with the target domain
                pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
                matches = re.findall(pattern, response.text)
                for m in matches:
                    # Filter out image files that look like emails
                    if not m.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                        self.emails.add(m.lower())
                return response.text
        except:
            pass
        return ""

    def run(self):
        print(f"\n  {M}╔════════════════════════════════════════════════════════════════╗{RS}")
        print(f"  {M}║                XOPHY DEEP EMAIL SCRAPER                        ║{RS}")
        print(f"  {M}╚════════════════════════════════════════════════════════════════╝{RS}")
        
        print(f"  {C}[*] Targeting: {W}{self.target}{RS}")
        print(f"  {C}[*] Status: Scanning landing page and common contact routes...{RS}\n")
        
        # 1. Scrape the main landing page
        html = self.scrape_page(self.target)
        
        # 2. Find common "Contact" or "About" links to crawl deeper
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href').lower()
                if 'contact' in href or 'about' in href or 'team' in href:
                    contact_url = urljoin(self.target, link.get('href'))
                    print(f"  {Y}[⇝]{RS} Following contact lead: {W}{contact_url}{RS}", end="\r")
                    self.scrape_page(contact_url)
        
        time.sleep(1) # Visual pause
        print(f"\n  {C}[ DISCOVERED FROM SITE SOURCE ]{RS}")
        
        if not self.emails:
            print(f"  {R}[!] No emails exposed in the public HTML of this site.{RS}")
        else:
            for email in sorted(self.emails):
                # Highlight emails that match the target domain
                color = G if self.domain in email else W
                print(f"  {G}✉{RS} {color}{email:<35}{RS} | {G}SRC: DIRECT{RS}")

        print(f"\n  {M}──────────────────────────────────────────────────────────────────{RS}")
        print(f"  {G}[✓] Extraction Complete. Unique Emails: {len(self.emails)}{RS}")

def run(target):
    harvester = XophyHarvester(target)
    harvester.run()
