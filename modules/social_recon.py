#!/usr/bin/env python3
"""
XOPHY Framework v3.0 - Advanced OSINT & Social Reconnaissance Engine
Author: Wasif Ali & Team
Description: Multi-threaded target profiling across 50+ high-fidelity platforms 
             with integrated stealth controls, evasion, and deep metadata extraction.
"""

import os
import sys
import json
import time
import random
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import cloudscraper

# Global Terminal Aesthetics
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner():
    banner = f"""
{CYAN}██╗  ██╗ ██████╗ ██████╗ ██╗  ██╗██╗   ██╗
╚██╗██╔╝██╔═══██╗██╔══██╗██║  ██║╚██╗ ██╔╝
 ╚███╔╝ ██║   ██║██████╔╝███████║ ╚████╔╝ 
 ██╔██╗ ██║   ██║██╔═══╝ ██╔══██║  ╚██╔╝  
██╔╝ ██╗╚██████╔╝██║     ██║  ██║   ██║   {RESET}{GREEN}v3.0 (Advanced Intel Engine){RESET}
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝   ╚═╝   
    """
    print(banner)

# 50+ High-Fidelity OSINT Target Registry (Categorized for Target Profiling)
PLATFORMS_REGISTRY = {
    # Core Dev & Code Repositories
    "GitHub": {"url": "https://github.com/{}", "error_indicator": "404 Not Found", "category": "Development"},
    "GitLab": {"url": "https://gitlab.com/{}", "error_indicator": "404 Not Found", "category": "Development"},
    "Bitbucket": {"url": "https://bitbucket.org/{}/", "error_indicator": "404 Not Found", "category": "Development"},
    "DockerHub": {"url": "https://hub.docker.com/u/{}", "error_indicator": "404 Not Found", "category": "Development"},
    "Codecademy": {"url": "https://www.codecademy.com/profiles/{}", "error_indicator": "404", "category": "Development"},
    "Dev.to": {"url": "https://dev.to/{}", "error_indicator": "404 Not Found", "category": "Development"},
    "Kaggle": {"url": "https://www.kaggle.com/{}", "error_indicator": "404", "category": "Data Science"},

    # Major Socials & Networking
    "Twitter/X": {"url": "https://x.com/{}", "error_indicator": "This account doesn’t exist", "category": "Social"},
    "Instagram": {"url": "https://www.instagram.com/{}/", "error_indicator": "Page Not Found", "category": "Social"},
    "LinkedIn": {"url": "https://www.linkedin.com/in/{}/", "error_indicator": "Page not found", "category": "Professional"},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "error_indicator": "nobody on Reddit goes by that name", "category": "Social"},
    "Pinterest": {"url": "https://www.pinterest.com/{}/", "error_indicator": "User not found", "category": "Social"},
    "Facebook": {"url": "https://www.facebook.com/{}", "error_indicator": "content isn't available", "category": "Social"},
    "TikTok": {"url": "https://www.tiktok.com/@{}", "error_indicator": "Couldn't find this account", "category": "Social"},
    "Snapchat": {"url": "https://www.snapchat.com/add/{}", "error_indicator": "not found", "category": "Social"},

    # Technical Forums & Q&A
    "StackOverflow": {"url": "https://stackoverflow.com/users/story/{}", "error_indicator": "404", "category": "Technical Forums"},
    "HackerNews": {"url": "https://news.ycombinator.com/user?id={}", "error_indicator": "No such user", "category": "Technical Forums"},
    "Quora": {"url": "https://www.quora.com/profile/{}", "error_indicator": "404 Not Found", "category": "Technical Forums"},
    "Medium": {"url": "https://medium.com/@{}", "error_indicator": "404", "category": "Publishing"},

    # Gaming & Video Platforms
    "Twitch": {"url": "https://www.twitch.tv/{}", "error_indicator": "404", "category": "Gaming"},
    "Steam": {"url": "https://steamcommunity.com/id/{}", "error_indicator": "The specified profile could not be found", "category": "Gaming"},
    "YouTube": {"url": "https://www.youtube.com/@{}", "error_indicator": "404 Not Found", "category": "Video"},
    "Vimeo": {"url": "https://vimeo.com/{}", "error_indicator": "404 Not Found", "category": "Video"},
    "DailyMotion": {"url": "https://www.dailymotion.com/{}", "error_indicator": "404", "category": "Video"},
    "Chess.com": {"url": "https://www.chess.com/member/{}", "error_indicator": "404", "category": "Gaming"},

    # Audio & Creative Media
    "SoundCloud": {"url": "https://soundcloud.com/{}", "error_indicator": "404 Not Found", "category": "Media"},
    "Spotify": {"url": "https://open.spotify.com/user/{}", "error_indicator": "404", "category": "Media"},
    "Bandcamp": {"url": "https://bandcamp.com/{}", "error_indicator": "404 Not Found", "category": "Media"},
    "Behance": {"url": "https://www.behance.net/{}", "error_indicator": "404", "category": "Creative"},
    "Dribbble": {"url": "https://dribbble.com/{}", "error_indicator": "404", "category": "Creative"},
    "Flickr": {"url": "https://www.flickr.com/photos/{}/", "error_indicator": "404", "category": "Media"},

    # Cybersecurity & IT Platforms
    "HackTheBox": {"url": "https://www.hackthebox.eu/profile/{}", "error_indicator": "404", "category": "Cybersecurity"},
    "TryHackMe": {"url": "https://tryhackme.com/p/{}", "error_indicator": "404", "category": "Cybersecurity"},
    "Bugcrowd": {"url": "https://bugcrowd.com/{}", "error_indicator": "404 Not Found", "category": "Cybersecurity"},
    "HackerOne": {"url": "https://hackerone.com/{}", "error_indicator": "404 Not Found", "category": "Cybersecurity"},

    # OSINT Leaks & Alternative Forums
    "Disqus": {"url": "https://disqus.com/by/{}/", "error_indicator": "404", "category": "Forums"},
    "Patreon": {"url": "https://www.patreon.com/{}", "error_indicator": "404", "category": "Financial"},
    "BuyMeACoffee": {"url": "https://www.buymeacoffee.com/{}", "error_indicator": "404", "category": "Financial"},
    "Linktree": {"url": "https://linktr.ee/{}", "error_indicator": "404", "category": "Aggregator"},
    "About.me": {"url": "https://about.me/{}", "error_indicator": "404", "category": "Aggregator"},
    "Pastebin": {"url": "https://pastebin.com/u/{}", "error_indicator": "404", "category": "Storage"},
    "Archive.org": {"url": "https://archive.org/details/@{}", "error_indicator": "404", "category": "Storage"},
    "SlideShare": {"url": "https://www.slideshare.net/{}", "error_indicator": "404", "category": "Corporate"},
    "Scribd": {"url": "https://www.scribd.com/user/{}", "error_indicator": "404", "category": "Corporate"},
    "ProductHunt": {"url": "https://www.producthunt.com/@{}", "error_indicator": "404", "category": "Corporate"},
    "Gfycat": {"url": "https://gfycat.com/@{}", "error_indicator": "404", "category": "Media"},
    "Imgur": {"url": "https://imgur.com/user/{}", "error_indicator": "404", "category": "Media"},
    "Letterboxd": {"url": "https://letterboxd.com/{}/", "error_indicator": "404", "category": "Social"},
    "LiveJournal": {"url": "https://{}.livejournal.com/", "error_indicator": "404", "category": "Publishing"},
    "WordPress": {"url": "https://{}.wordpress.com/", "error_indicator": "Do you want to register", "category": "Publishing"}
}

class SocialReconEngine:
    def __init__(self, username, stealth=False, deep=False, threads=15):
        self.username = username
        self.stealth = stealth
        self.deep = deep
        self.threads = threads
        self.results = {}
        
        # Safe Fallback List of Linux & Windows Browser Signatures
        self.fallback_agents = [
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/21010101 Firefox/115.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]
        
        # Safely attempt to initialize fake_useragent locally
        try:
            from fake_useragent import UserAgent
            self.ua = UserAgent()
        except Exception:
            self.ua = None
            
        self.scraper = cloudscraper.create_scraper()

    def _get_headers(self):
        try:
            user_agent = self.ua.random if self.ua else random.choice(self.fallback_agents)
        except Exception:
            user_agent = random.choice(self.fallback_agents)

        return {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def _deep_parse(self, html_content):
        intelligence = {"meta_description": "", "title": ""}
        if not html_content:
            return intelligence
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title signature
        if soup.title and soup.title.string:
            intelligence["title"] = soup.title.string.strip()

        # Extract Meta description configurations
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc and meta_desc.get("content"):
            intelligence["meta_description"] = meta_desc["content"].strip()
            
        return intelligence

    def scan_platform(self, platform_name, config):
        target_url = config["url"].format(self.username)
        headers = self._get_headers()
        
        if self.stealth:
            time.sleep(random.uniform(1.0, 3.0))
            
        try:
            response = self.scraper.get(target_url, headers=headers, timeout=8, allow_redirects=True)
            
            is_valid = False
            if response.status_code == 200:
                if config["error_indicator"].lower() not in response.text.lower():
                    is_valid = True
            elif response.status_code in [403, 429]:
                return platform_name, {"status": "WAF Protection/Cloudflare Detected", "found": False, "category": config["category"]}
                
            if is_valid:
                data = {
                    "status": "Target Profile Identified",
                    "found": True,
                    "url": target_url,
                    "category": config["category"]
                }
                if self.deep:
                    data["intelligence"] = self._deep_parse(response.text)
                return platform_name, data
            else:
                return platform_name, {"status": "No Account Found", "found": False, "category": config["category"]}
                
        except requests.exceptions.RequestException:
            return platform_name, {"status": "Connection Error", "found": False, "category": config["category"]}

    def execute_recon(self):
        print(f"[*] Thread pool initiated with {BOLD}{self.threads}{RESET} active workers.")
        print(f"[*] Total target nodes mapped: {CYAN}{len(PLATFORMS_REGISTRY)}{RESET}")
        print(f"[*] Target handle: {YELLOW}@{self.username}{RESET}\n")
        
        found_count = 0
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_platform = {
                executor.submit(self.scan_platform, name, cfg): name 
                for name, cfg in PLATFORMS_REGISTRY.items()
            }
            
            for future in as_completed(future_to_platform):
                platform_name = future_to_platform[future]
                try:
                    name, data = future.result()
                    self.results[name] = data
                    
                    if data["found"]:
                        found_count += 1
                        print(f"[{GREEN}➔{RESET}] {BOLD}{name:<15}{RESET} [{CYAN}{data['category']}{RESET}]: {GREEN}FOUND{RESET} -> {data['url']}")
                        if self.deep and "intelligence" in data:
                            title = data["intelligence"]["title"]
                            desc = data["intelligence"]["meta_description"]
                            if title:
                                print(f"    └── {YELLOW}Title Signature:{RESET} {title}")
                            if desc:
                                print(f"    └── {BLUE}Bio/Metadata Summary:{RESET} {desc[:90]}...")
                except Exception as exc:
                    print(f"[{RED}!{RESET}] Platform {platform_name} generated an exception: {exc}")
                    
        print(f"\n[*] Recon Complete: Identified {GREEN}{found_count}{RESET} active accounts out of {len(PLATFORMS_REGISTRY)} platforms.")

    def export_report(self):
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        filename = f"{report_dir}/recon_{self.username}_{int(time.time())}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        print(f"[+] Advanced intelligence payload serialized to: {BLUE}{filename}{RESET}")


def run(target):
    """Core entry point hook for the XOPHY Framework CLI."""
    engine = SocialReconEngine(
        username=target, 
        stealth=False, 
        deep=True,     
        threads=15     
    )
    
    start_time = time.time()
    engine.execute_recon()
    engine.export_report()
    print(f"[*] Module execution completed in {time.time() - start_time:.2f} seconds.\n")


def main():
    """Standalone CLI launcher fallback."""
    print_banner()
    parser = argparse.ArgumentParser(description="XOPHY Framework v3.0 - Recon Engine")
    parser.add_argument("target", help="Target username or handle to query")
    parser.add_argument("--stealth", action="store_true", help="Enable randomized delay patterns to evade WAFs")
    parser.add_argument("--deep", action="store_true", help="Extract profile text metadata signatures")
    parser.add_argument("--threads", type=int, default=15, help="Concurrent scanner threads configuration")
    
    args = parser.parse_args()
    engine = SocialReconEngine(username=args.target, stealth=args.stealth, deep=args.deep, threads=args.threads)
    
    start_time = time.time()
    engine.execute_recon()
    engine.export_report()
    print(f"[*] Standalone audit run completed in {time.time() - start_time:.2f} seconds.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Operations interrupted by keyboard signal. Exiting execution path safely.{RESET}")
        sys.exit(1)
