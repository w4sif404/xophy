#!/usr/bin/env python3
"""
Xophy Elite Web Crawler - Advanced Reconnaissance Module
With Beautiful Xophy-style Output Formatting
"""

import requests
import re
import urllib3
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter, defaultdict
import time
import sys
from datetime import datetime

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Xophy Colors
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
R = '\033[91m'  # Red
C = '\033[96m'  # Cyan
W = '\033[97m'  # White
M = '\033[95m'  # Magenta
RS = '\033[0m'  # Reset

def run(target, max_pages=200, threads=30):
    """Main web crawler function with Xophy output format"""
    
    # Normalize target
    if not target.startswith(('http://', 'https://')):
        target = f"https://{target}"
    
    domain = urlparse(target).netloc
    
    # Initialize data structures
    visited = set()
    results = {
        'urls': set(),
        'internal_links': set(),
        'external_links': set(),
        'js_files': set(),
        'css_files': set(),
        'images': set(),
        'documents': set(),
        'emails': set(),
        'subdomains': set(),
        'api_endpoints': set(),
        'hidden_routes': set(),
        'technologies': set(),
        'ip_addresses': set(),
        'parameters': set(),
        'forms': []
    }
    
    # Print header
    print(f"\n  {C}[WEB SPIDER] Target: {domain}{RS}")
    print(f"  {C}{'━'*60}{RS}")
    print(f"\n  {C}[*] Recursive crawler active. Gathering intelligence...{RS}\n")
    
    # Session setup
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    
    def extract_tech(response):
        """Extract technology stack"""
        techs = set()
        html = response.text.lower()
        headers = str(response.headers).lower()
        
        # Server detection
        if 'apache' in headers:
            techs.add('Apache')
        if 'nginx' in headers:
            techs.add('Nginx')
        if 'cloudflare' in headers:
            techs.add('Cloudflare')
        
        # CMS detection
        if 'wp-content' in html or 'wp-includes' in html:
            techs.add('WordPress')
        if 'drupal' in html:
            techs.add('Drupal')
        if 'joomla' in html:
            techs.add('Joomla')
        
        # PHP detection
        if '.php' in html or 'x-powered-by: php' in headers:
            techs.add('PHP')
        
        return techs
    
    def extract_emails(text):
        """Extract email addresses"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = set(re.findall(email_pattern, text))
        # Filter out false positives
        emails = {e for e in emails if not e.endswith(('.png', '.jpg', '.gif', '.svg', '.css', '.js'))}
        return emails
    
    def extract_ips(text):
        """Extract IP addresses (especially internal)"""
        # Private IP patterns
        private_ip_pattern = r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[0-1])|192\.168)\.\d{1,3}\.\d{1,3}\b'
        ips = set(re.findall(private_ip_pattern, text))
        return ips
    
    def extract_hidden_routes(text):
        """Extract hidden API routes and endpoints"""
        route_patterns = [
            r'/(?:api|v[0-9]|wp-json|admin|config|rest|graphql)/[a-zA-Z0-9\-_/]+',
            r'"/[a-zA-Z0-9\-_]+/[0-9]+"',
            r'"/wp-json/wp/v2/[a-z-]+"',
        ]
        routes = set()
        for pattern in route_patterns:
            matches = re.findall(pattern, text)
            routes.update(matches)
        return routes
    
    def extract_subdomains(url):
        """Extract subdomains from URLs"""
        parsed = urlparse(url)
        if parsed.netloc and domain in parsed.netloc and parsed.netloc != domain:
            return parsed.netloc
        return None
    
    def crawl_worker(url):
        """Worker function for crawling"""
        if url in visited or len(visited) >= max_pages:
            return []
        
        visited.add(url)
        
        try:
            response = session.get(url, timeout=8, verify=False, allow_redirects=True)
            
            if response.status_code == 200:
                # Show progress
                print(f"  {G}[SCANNING]{RS} {url[:70]}...", end="\r")
                
                # Extract data
                emails = extract_emails(response.text)
                ips = extract_ips(response.text)
                techs = extract_tech(response)
                hidden_routes = extract_hidden_routes(response.text)
                
                # Update results
                results['emails'].update(emails)
                results['ip_addresses'].update(ips)
                results['technologies'].update(techs)
                results['hidden_routes'].update(hidden_routes)
                results['urls'].add(url)
                
                # Parse HTML for links
                soup = BeautifulSoup(response.text, 'html.parser')
                links = []
                
                for tag in soup.find_all(['a', 'link', 'script', 'img']):
                    attr = tag.get('href') or tag.get('src')
                    if not attr:
                        continue
                    
                    full_url = urljoin(url, attr)
                    parsed_url = urlparse(full_url)
                    
                    # Check for subdomains
                    sub = extract_subdomains(full_url)
                    if sub:
                        results['subdomains'].add(sub)
                    
                    # Categorize by extension
                    if full_url.endswith(('.js', '.jsx', '.ts')):
                        results['js_files'].add(full_url)
                    elif full_url.endswith(('.css', '.scss', '.sass')):
                        results['css_files'].add(full_url)
                    elif full_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')):
                        results['images'].add(full_url)
                    elif full_url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt')):
                        results['documents'].add(full_url)
                    elif full_url.endswith(('.zip', '.tar', '.gz', '.sql', '.dump', '.log', '.env')):
                        results['documents'].add(full_url)
                    
                    # Check if internal link
                    if parsed_url.netloc == domain or not parsed_url.netloc:
                        if full_url not in visited and not full_url.endswith(('.jpg', '.png', '.gif', '.css', '.js')):
                            links.append(full_url)
                        results['internal_links'].add(full_url)
                    elif parsed_url.netloc:
                        results['external_links'].add(full_url)
                
                # Extract API endpoints
                api_pattern = r'/(?:api|rest|graphql|swagger|openapi|v[0-9])/'
                for link in links:
                    if re.search(api_pattern, link):
                        results['api_endpoints'].add(link)
                
                # Extract parameters
                if urlparse(url).query:
                    params = parse_qs(urlparse(url).query)
                    results['parameters'].update(params.keys())
                
                return links
            
        except Exception as e:
            pass
        
        return []
    
    # Start crawling
    queue = [target]
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while queue and len(visited) < max_pages:
            # Process batch
            batch = queue[:threads]
            queue = queue[threads:]
            
            futures = [executor.submit(crawl_worker, url) for url in batch]
            
            for future in as_completed(futures):
                new_links = future.result()
                for link in new_links:
                    if link not in visited and link not in queue:
                        queue.append(link)
    
    # Print the Xophy report
    print(f"\n\n  {M}╔════════════════════════════════════════════════════════════════╗{RS}")
    print(f"  {M}║                XOPHY RECONNAISSANCE REPORT                     ║{RS}")
    print(f"  {M}╚════════════════════════════════════════════════════════════════╝{RS}")
    
    # Technologies section
    if results['technologies']:
        print(f"\n  {C}[ SYSTEM ARCHITECTURE ]{RS}")
        for tech in sorted(results['technologies']):
            print(f"  {C}❯{RS} {W}{tech}{RS}")
    
    # Critical leaks (IP addresses)
    if results['ip_addresses']:
        print(f"\n  {R}[ CRITICAL INFRASTRUCTURE LEAKS ]{RS}")
        for ip in sorted(results['ip_addresses']):
            print(f"  {R}☠{RS} {W}{ip}{RS}")
    
    # Subdomains
    if results['subdomains']:
        print(f"\n  {Y}[ DISCOVERED SUBDOMAINS ]{RS}")
        for sub in sorted(results['subdomains']):
            print(f"  {Y}🌐{RS} {W}{sub}{RS}")
    
    # Hidden API routes
    if results['hidden_routes']:
        print(f"\n  {G}[ HIDDEN API & APP ROUTES ]{RS}")
        for route in sorted(results['hidden_routes'])[:20]:  # Limit to 20
            print(f"  {G}🔗{RS} {W}{route}{RS}")
    
    # API endpoints
    if results['api_endpoints']:
        print(f"\n  {M}[ VERIFIED API ENDPOINTS ]{RS}")
        for api in sorted(results['api_endpoints'])[:15]:
            print(f"  {M}✔{RS} {W}{api}{RS}")
    
    # Emails
    if results['emails']:
        print(f"\n  {C}[ TARGET CONTACT LIST ]{RS}")
        for email in sorted(results['emails']):
            print(f"  {C}✉{RS} {W}{email}{RS}")
    
    # Parameters discovered
    if results['parameters']:
        print(f"\n  {Y}[ URL PARAMETERS ]{RS}")
        for param in sorted(results['parameters'])[:15]:
            print(f"  {Y}📝{RS} {W}{param}{RS}")
    
    # Summary statistics
    print(f"\n  {M}──────────────────────────────────────────────────────────────────{RS}")
    print(f"  {C}📊 Summary:{RS}")
    print(f"  • Pages crawled: {len(visited)}")
    print(f"  • Internal links: {len(results['internal_links'])}")
    print(f"  • External links: {len(results['external_links'])}")
    print(f"  • Images found: {len(results['images'])}")
    print(f"  • Documents: {len(results['documents'])}")
    print(f"  • JS files: {len(results['js_files'])}")
    print(f"  • CSS files: {len(results['css_files'])}")
    print(f"  • Hidden routes: {len(results['hidden_routes'])}")
    print(f"  • API endpoints: {len(results['api_endpoints'])}")
    print(f"  • Emails: {len(results['emails'])}")
    print(f"  • Subdomains: {len(results['subdomains'])}")
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"xophy_crawl_{domain.replace('.', '_')}_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Xophy Web Crawl Report - {target}\n")
        f.write(f"{'='*70}\n\n")
        
        f.write("TECHNOLOGIES:\n")
        for tech in sorted(results['technologies']):
            f.write(f"  - {tech}\n")
        
        f.write("\nSUBDOMAINS:\n")
        for sub in sorted(results['subdomains']):
            f.write(f"  - {sub}\n")
        
        f.write("\nEMAILS:\n")
        for email in sorted(results['emails']):
            f.write(f"  - {email}\n")
        
        f.write("\nHIDDEN ROUTES:\n")
        for route in sorted(results['hidden_routes']):
            f.write(f"  - {route}\n")
        
        f.write("\nAPI ENDPOINTS:\n")
        for api in sorted(results['api_endpoints']):
            f.write(f"  - {api}\n")
    
    print(f"\n  {G}✓ Results saved to: {filename}{RS}")
    print(f"  {M}──────────────────────────────────────────────────────────────────{RS}\n")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        target = input(f"  {C}◎ Enter target domain/IP → {RS}")
        run(target)
