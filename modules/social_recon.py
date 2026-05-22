import requests
import time

# ANSI Colors
G, Y, R, C, W, M, RS = "\033[92m", "\033[93m", "\033[91m", "\033[96m", "\033[97m", "\033[95m", "\033[0m"

class XophySocialRecon:
    def __init__(self, username):
        self.username = username
        # Real URLs to check
        self.targets = {
            "Instagram": f"https://www.instagram.com/{username}/",
            "Twitter/X": f"https://x.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}/",
            "YouTube": f"https://www.youtube.com/@{username}"
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def scan(self):
        print(f"  {C}[*] Initiating deep probe for handle: {W}{self.username}{RS}\n")
        
        found_count = 0
        for platform, url in self.targets.items():
            print(f"  {Y}[?]{RS} Checking {platform}...", end="\r")
            try:
                # We use allow_redirects=False to catch 404s accurately
                res = requests.get(url, headers=self.headers, timeout=10, allow_redirects=True)
                
                # Check status code
                if res.status_code == 200:
                    # Some sites (like Instagram) return 200 even for errors, 
                    # so we check for common "Error" text in the page
                    if "Page Not Found" not in res.text and "Couldn't find this page" not in res.text:
                        print(f"  {G}[+] {platform:<12} : {W}{url}{RS}")
                        found_count += 1
                    else:
                        print(f"  {R}[-] {platform:<12} : {RS}Not Found", end="\r")
                else:
                    print(f"  {R}[-] {platform:<12} : {RS}Not Found", end="\r")
            except Exception:
                print(f"  {R}[!] {platform:<12} : {RS}Connection Error", end="\r")
            
            time.sleep(0.5) # Prevent getting IP banned/throttled

        return found_count

    def run(self):
        print(f"\n  {M}╔════════════════════════════════════════════════════════════════╗{RS}")
        print(f"  {M}║                XOPHY SOCIAL MEDIA PROBE                        ║{RS}")
        print(f"  {M}╚════════════════════════════════════════════════════════════════╝{RS}")
        
        total = self.scan()
        
        print(f"\n  {M}──────────────────────────────────────────────────────────────────{RS}")
        if total > 0:
            print(f"  {G}[✓] Scan complete. {total} active profiles identified.{RS}")
        else:
            print(f"  {R}[!] No profiles identified for {self.username}.{RS}")

def run(username):
    recon = XophySocialRecon(username)
    recon.run()
