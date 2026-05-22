#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              XOPHY QUANTUM SPIDER v3.0 - NEXT-GEN RECONNAISSANCE              ║
║                         [ DEEP WEB | DARK WEB | SURFACE ]                     ║
║                            Author: w45if_4o4                                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import re
import urllib3
import json
import time
import hashlib
import base64
import random
import string
import threading
import queue
from urllib.parse import urlparse, urljoin, parse_qs, quote, unquote
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
import os
import sys
import socket
import ssl
import dns.resolver
import whois

# Suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ──────────────────────────────────────────────────────────────────────────────
# COLORS & STYLING
# ──────────────────────────────────────────────────────────────────────────────

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'
    RESET = '\033[0m'

@dataclass
class DiscoveredAsset:
    url: str
    type: str
    status_code: int
    size: int
    found_in: str
    timestamp: datetime = field(default_factory=datetime.now)

class QuantumSpider:
    """Next-Gen Web Spider with Deep Discovery Capabilities"""
    
    def __init__(self, target: str, max_depth: int = 5, max_pages: int = 500, threads: int = 50):
        self.target = target if target.startswith(('http://', 'https://')) else f'https://{target}'
        self.domain = urlparse(self.target).netloc
        self.base_domain = self.domain.replace('www.', '')
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.threads = threads
        self.start_time = None
        
        # Session with rotating headers
        self.session = self._create_session()
        
        # Data storage
        self.discovered = {
            'urls': set(),
            'internal': set(),
            'external': set(),
            'js_files': set(),
            'css_files': set(),
            'images': set(),
            'documents': set(),
            'archives': set(),
            'backup_files': set(),
            'config_files': set(),
            'api_endpoints': set(),
            'graphql_endpoints': set(),
            'admin_panels': set(),
            'login_panels': set(),
            'subdomains': set(),
            'ip_addresses': set(),
            'emails': set(),
            'phone_numbers': set(),
            'social_media': set(),
            'technologies': defaultdict(set),
            'parameters': set(),
            'headers': defaultdict(list),
            'cookies': set(),
            'comments': [],
            'metadata': {},
            's3_buckets': set(),
            'cloudfront_urls': set(),
            'hidden_directories': set(),
            'interesting_paths': set(),
        }
        
        # Progress tracking
        self.visited = set()
        self.to_visit = queue.Queue()
        self.to_visit.put((self.target, 0))
        self.lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'requests': 0,
            'success': 0,
            'errors': 0,
            'redirects': 0,
            'data_transferred': 0,
            'start_time': None,
            'end_time': None,
        }
        
        # Wordlists for fuzzing
        self.wordlists = self._load_wordlists()
        
    def _create_session(self) -> requests.Session:
        """Create session with rotating headers"""
        session = requests.Session()
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
        ]
        
        session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
        
        return session
    
    def _load_wordlists(self) -> Dict:
        """Load wordlists for fuzzing"""
        return {
            'admin_paths': [
                'admin', 'administrator', 'adminpanel', 'cp', 'cpanel', 'webadmin',
                'dashboard', 'controlpanel', 'manage', 'operator', 'sysadmin'
            ],
            'api_paths': [
                'api', 'v1', 'v2', 'v3', 'rest', 'graphql', 'swagger', 'openapi',
                'docs', 'apidocs', 'api-docs', 'redoc', 'json', 'data', 'service'
            ],
            'backup_extensions': [
                '.bak', '.old', '.backup', '~', '.swp', '.swo', '.save', '.orig',
                '.sql', '.dump', '.tar', '.gz', '.zip', '.7z', '.rar'
            ],
            'config_files': [
                '.env', '.git/config', '.aws/credentials', '.ssh/id_rsa',
                'wp-config.php', 'config.php', 'database.yml', 'secrets.yml',
                'credentials.json', 'service-account.json', '.htpasswd'
            ],
            'sensitive_dirs': [
                '.git', '.svn', '.hg', '.env', 'backup', 'temp', 'tmp', 'logs',
                'debug', 'test', 'dev', 'staging', 'private', 'secret', 'hidden'
            ],
            'common_extensions': ['php', 'asp', 'aspx', 'jsp', 'do', 'action', 'html', 'htm']
        }
    
    def fetch_url(self, url: str, depth: int) -> Optional[Tuple[requests.Response, int]]:
        """Fetch URL with error handling and redirect tracking"""
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=10, verify=False, allow_redirects=True)
            elapsed = time.time() - start_time
            
            with self.lock:
                self.stats['requests'] += 1
                self.stats['data_transferred'] += len(response.content)
                
                if response.status_code == 200:
                    self.stats['success'] += 1
                elif response.status_code in [301, 302, 307, 308]:
                    self.stats['redirects'] += 1
                else:
                    self.stats['errors'] += 1
            
            return response, depth
            
        except Exception as e:
            with self.lock:
                self.stats['errors'] += 1
            return None, depth
    
    def extract_all_links(self, html: str, base_url: str) -> Set[str]:
        """Extract all links from HTML (including JS, CSS, Images)"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        # All possible link attributes
        tags_with_links = {
            'a': 'href', 'link': 'href', 'script': 'src', 'img': 'src',
            'iframe': 'src', 'form': 'action', 'area': 'href', 'base': 'href'
        }
        
        for tag, attr in tags_with_links.items():
            for element in soup.find_all(tag):
                if element.get(attr):
                    full_url = urljoin(base_url, element[attr])
                    if full_url.startswith(('http://', 'https://')):
                        links.add(full_url)
        
        # Extract from inline JavaScript
        for script in soup.find_all('script'):
            if script.string:
                # Find URLs in JS
                js_urls = re.findall(r'["\'](https?://[^\s"\']+)["\']', script.string)
                links.update(js_urls)
                
                # Find API calls
                api_calls = re.findall(r'/(?:api|v\d+|rest)/[^\s"\']+', script.string)
                for api in api_calls:
                    links.add(urljoin(base_url, api))
        
        # Extract from CSS
        for style in soup.find_all('style'):
            if style.string:
                css_urls = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', style.string)
                for css_url in css_urls:
                    if css_url.startswith(('http://', 'https://')):
                        links.add(css_url)
                    elif css_url.startswith('/'):
                        links.add(urljoin(base_url, css_url))
        
        # Extract from meta tags
        for meta in soup.find_all('meta', attrs={'http-equiv': 'refresh'}):
            content = meta.get('content', '')
            if 'url=' in content.lower():
                redirect_url = content.split('url=')[-1]
                links.add(urljoin(base_url, redirect_url))
        
        return links
    
    def analyze_page(self, url: str, response: requests.Response, depth: int):
        """Deep analysis of discovered page"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ──────────────────────────────────────────────────────────────────────
        # 1. TECHNOLOGY DETECTION
        # ──────────────────────────────────────────────────────────────────────
        techs = set()
        html_lower = response.text.lower()
        headers_lower = str(response.headers).lower()
        
        tech_signatures = {
            'Web Servers': {
                'Apache': 'apache', 'Nginx': 'nginx', 'IIS': 'iis',
                'Cloudflare': 'cloudflare', 'AWS': 'amazonaws'
            },
            'CMS': {
                'WordPress': 'wp-content', 'Drupal': 'drupal', 'Joomla': 'joomla',
                'Magento': 'magento', 'Shopify': 'shopify'
            },
            'Frameworks': {
                'React': 'react', 'Vue.js': 'vue', 'Angular': 'ng-',
                'Django': 'django', 'Laravel': 'laravel', 'Rails': 'ruby on rails'
            },
            'Analytics': {
                'Google Analytics': 'google-analytics', 'Facebook Pixel': 'fbq',
                'Hotjar': 'hotjar', 'Mixpanel': 'mixpanel'
            },
            'Security': {
                'Cloudflare': 'cf-ray', 'Sucuri': 'sucuri', 'ModSecurity': 'mod_security'
            }
        }
        
        for category, tools in tech_signatures.items():
            for tool, signature in tools.items():
                if signature in html_lower or signature in headers_lower:
                    self.discovered['technologies'][category].add(tool)
        
        # ──────────────────────────────────────────────────────────────────────
        # 2. SENSITIVE DATA EXTRACTION
        # ──────────────────────────────────────────────────────────────────────
        
        # Emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = set(re.findall(email_pattern, response.text))
        emails = {e for e in emails if not e.endswith(('.png', '.jpg', '.gif', '.css', '.js', '.svg'))}
        self.discovered['emails'].update(emails)
        
        # Phone numbers
        phone_pattern = r'\+?[\d\s\-\(\)]{10,20}'
        phones = set(re.findall(phone_pattern, response.text))
        self.discovered['phone_numbers'].update([p for p in phones if len(p) > 8])
        
        # IP Addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = set(re.findall(ip_pattern, response.text))
        self.discovered['ip_addresses'].update(ips)
        
        # Social Media Links
        social_patterns = {
            'facebook': r'facebook\.com/[a-zA-Z0-9.]+',
            'twitter': r'twitter\.com/[a-zA-Z0-9_]+',
            'instagram': r'instagram\.com/[a-zA-Z0-9_.]+',
            'linkedin': r'linkedin\.com/(?:company|in)/[a-zA-Z0-9-]+',
            'github': r'github\.com/[a-zA-Z0-9-]+',
        }
        
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, response.text, re.I)
            for match in matches:
                self.discovered['social_media'].add(f"{platform}: {match}")
        
        # ──────────────────────────────────────────────────────────────────────
        # 3. API & ENDPOINT DISCOVERY
        # ──────────────────────────────────────────────────────────────────────
        
        # API patterns
        api_patterns = [
            r'/(?:api|v\d+|rest|graphql)/[^\s"\']+',
            r'"https?://[^"]+/(?:api|v\d+)/[^"]+"',
            r"['\"]/?(?:api|rest|graphql)/[a-zA-Z0-9\-_/]+['\"]",
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, response.text, re.I)
            for match in matches:
                full_url = urljoin(url, match)
                self.discovered['api_endpoints'].add(full_url)
        
        # GraphQL detection
        if 'graphql' in response.text.lower() or '__schema' in response.text:
            self.discovered['graphql_endpoints'].add(url)
        
        # ──────────────────────────────────────────────────────────────────────
        # 4. ADMIN & LOGIN PANELS
        # ──────────────────────────────────────────────────────────────────────
        
        admin_keywords = ['admin', 'administrator', 'cpanel', 'dashboard', 'control']
        login_keywords = ['login', 'signin', 'logon', 'auth', 'authenticate']
        
        for keyword in admin_keywords:
            if keyword in url.lower():
                self.discovered['admin_panels'].add(url)
        
        for keyword in login_keywords:
            if keyword in url.lower():
                self.discovered['login_panels'].add(url)
        
        # Find forms that might be login
        for form in soup.find_all('form'):
            action = form.get('action', '')
            if any(k in action.lower() for k in login_keywords):
                self.discovered['login_panels'].add(urljoin(url, action))
        
        # ──────────────────────────────────────────────────────────────────────
        # 5. ASSET DISCOVERY
        # ──────────────────────────────────────────────────────────────────────
        
        # JavaScript files
        for script in soup.find_all('script', src=True):
            js_url = urljoin(url, script['src'])
            self.discovered['js_files'].add(js_url)
            
            # Check for source maps
            try:
                js_response = self.session.get(js_url, timeout=5)
                if 'sourceMappingURL' in js_response.text:
                    map_match = re.search(r'sourceMappingURL=(.+\.map)', js_response.text)
                    if map_match:
                        self.discovered['hidden_routes'].add(map_match.group(1))
            except:
                pass
        
        # CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            if link.get('href'):
                self.discovered['css_files'].add(urljoin(url, link['href']))
        
        # Images
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            self.discovered['images'].add(img_url)
        
        # Documents
        doc_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']
        for link in soup.find_all('a', href=True):
            href = link['href']
            if any(href.lower().endswith(ext) for ext in doc_extensions):
                self.discovered['documents'].add(urljoin(url, href))
        
        # Archives
        archive_extensions = ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar']
        for link in soup.find_all('a', href=True):
            href = link['href']
            if any(href.lower().endswith(ext) for ext in archive_extensions):
                self.discovered['archives'].add(urljoin(url, href))
        
        # ──────────────────────────────────────────────────────────────────────
        # 6. COMMENTS & HIDDEN DATA
        # ──────────────────────────────────────────────────────────────────────
        
        # HTML Comments
        comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text)
        for comment in comments:
            if comment.strip():
                self.discovered['comments'].append({
                    'url': url,
                    'content': comment.strip()[:200]
                })
                
                # Check for TODO/FIXME/SECURITY notes
                if re.search(r'TODO|FIXME|HACK|BUG|SECURITY|PASSWORD|API_KEY', comment, re.I):
                    self.discovered['interesting_paths'].add(f"Comment: {comment[:100]}")
        
        # Meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            if name and content:
                self.discovered['metadata'][name] = content
        
        # ──────────────────────────────────────────────────────────────────────
        # 7. SUBDOMAIN DISCOVERY
        # ──────────────────────────────────────────────────────────────────────
        
        subdomain_pattern = rf'([a-zA-Z0-9_-]+)\.{re.escape(self.base_domain)}'
        subdomains = set(re.findall(subdomain_pattern, response.text, re.I))
        for sub in subdomains:
            self.discovered['subdomains'].add(f"{sub}.{self.base_domain}")
        
        # ──────────────────────────────────────────────────────────────────────
        # 8. PARAMETERS & QUERY STRINGS
        # ──────────────────────────────────────────────────────────────────────
        
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            self.discovered['parameters'].update(params.keys())
        
        # ──────────────────────────────────────────────────────────────────────
        # 9. HEADERS & COOKIES
        # ──────────────────────────────────────────────────────────────────────
        
        for header, value in response.headers.items():
            self.discovered['headers'][header].append(value)
        
        for cookie in response.cookies:
            self.discovered['cookies'].add(f"{cookie.name}={cookie.value}")
        
        # ──────────────────────────────────────────────────────────────────────
        # 10. CLOUD SERVICES DETECTION
        # ──────────────────────────────────────────────────────────────────────
        
        cloud_patterns = {
            's3_buckets': r'([a-z0-9.-]+)\.s3\.amazonaws\.com',
            'cloudfront': r'([a-z0-9]+)\.cloudfront\.net',
            'azure': r'([a-z0-9]+)\.blob\.core\.windows\.net',
            'gcp': r'([a-z0-9]+)\.storage\.googleapis\.com',
        }
        
        for service, pattern in cloud_patterns.items():
            matches = re.findall(pattern, response.text, re.I)
            for match in matches:
                if service == 's3_buckets':
                    self.discovered['s3_buckets'].add(match)
                elif service == 'cloudfront':
                    self.discovered['cloudfront_urls'].add(match)
    
    def fuzz_endpoints(self):
        """Fuzz for hidden endpoints and directories"""
        print(f"\n  {Colors.CYAN}[*] Fuzzing for hidden endpoints...{Colors.RESET}")
        
        found = set()
        
        # Test admin paths
        for path in self.wordlists['admin_paths'][:20]:
            url = f"{self.target}/{path}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    self.discovered['admin_panels'].add(url)
                    print(f"    {Colors.GREEN}[+] Found admin: {url}{Colors.RESET}")
                elif resp.status_code in [401, 403]:
                    self.discovered['admin_panels'].add(f"{url} (Auth Required)")
                    print(f"    {Colors.YELLOW}[!] Auth protected: {url}{Colors.RESET}")
            except:
                pass
        
        # Test API paths
        for path in self.wordlists['api_paths'][:20]:
            url = f"{self.target}/{path}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    self.discovered['api_endpoints'].add(url)
                    print(f"    {Colors.GREEN}[+] Found API: {url}{Colors.RESET}")
            except:
                pass
        
        # Check for sensitive files
        for config in self.wordlists['config_files'][:10]:
            url = f"{self.target}/{config}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    self.discovered['config_files'].add(url)
                    print(f"    {Colors.RED}[!!!] EXPOSED CONFIG: {url}{Colors.RESET}")
            except:
                pass
        
        return found
    
    def crawl_worker(self):
        """Worker thread for crawling"""
        while not self.to_visit.empty():
            try:
                url, depth = self.to_visit.get(timeout=1)
            except:
                break
            
            if url in self.visited or len(self.visited) >= self.max_pages:
                continue
            
            with self.lock:
                self.visited.add(url)
                self.discovered['urls'].add(url)
            
            # Fetch URL
            result = self.fetch_url(url, depth)
            if not result:
                continue
            
            response, current_depth = result
            
            if response.status_code == 200:
                # Analyze page
                self.analyze_page(url, response, current_depth)
                
                # Extract links for deeper crawling
                if current_depth < self.max_depth:
                    links = self.extract_all_links(response.text, url)
                    
                    for link in links:
                        parsed = urlparse(link)
                        
                        # Only follow internal links
                        if parsed.netloc == self.domain or not parsed.netloc:
                            if link not in self.visited:
                                with self.lock:
                                    self.discovered['internal'].add(link)
                                self.to_visit.put((link, current_depth + 1))
                        else:
                            with self.lock:
                                self.discovered['external'].add(link)
                
                # Show progress
                with self.lock:
                    crawled = len(self.visited)
                    if crawled % 10 == 0:
                        print(f"  {Colors.CYAN}[*] Crawled: {crawled}/{self.max_pages} | Found: {len(self.discovered['internal'])} links | Depth: {current_depth}{Colors.RESET}")
    
    def generate_shocking_report(self):
        """Generate an eye-opening, shocking report"""
        elapsed = time.time() - self.start_time
        
        print(f"\n\n  {Colors.RED}{Colors.BOLD}{'█'*70}{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}║              💀 XOPHY QUANTUM SPIDER - RECONNAISSANCE REPORT 💀              ║{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}{'█'*70}{Colors.RESET}")
        
        # Target Info
        print(f"\n  {Colors.CYAN}📡 TARGET INFORMATION{Colors.RESET}")
        print(f"  {'─'*66}")
        print(f"  {Colors.WHITE}Target URL:     {self.target}{Colors.RESET}")
        print(f"  {Colors.WHITE}Domain:         {self.domain}{Colors.RESET}")
        print(f"  {Colors.WHITE}Scan Duration:  {elapsed:.2f} seconds{Colors.RESET}")
        print(f"  {Colors.WHITE}Pages Crawled:  {len(self.visited)}/{self.max_pages}{Colors.RESET}")
        
        # Statistics
        print(f"\n  {Colors.GREEN}📊 STATISTICS{Colors.RESET}")
        print(f"  {'─'*66}")
        print(f"  {Colors.WHITE}• Requests Sent:     {self.stats['requests']}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Successful:        {self.stats['success']}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Errors:            {self.stats['errors']}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Redirects:         {self.stats['redirects']}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Data Transferred:  {self.stats['data_transferred'] / 1024 / 1024:.2f} MB{Colors.RESET}")
        
        # Critical Findings - SHOCKING PART
        print(f"\n  {Colors.RED}{Colors.BOLD}🔥 CRITICAL / SHOCKING FINDINGS 🔥{Colors.RESET}")
        print(f"  {'─'*66}")
        
        shock_factors = []
        
        if self.discovered['config_files']:
            shock_factors.append(f"  {Colors.RED}[!!!] EXPOSED CONFIGURATION FILES: {len(self.discovered['config_files'])}{Colors.RESET}")
            for cfg in list(self.discovered['config_files'])[:5]:
                shock_factors.append(f"       → {cfg}")
        
        if self.discovered['admin_panels']:
            shock_factors.append(f"  {Colors.RED}[!!!] EXPOSED ADMIN PANELS: {len(self.discovered['admin_panels'])}{Colors.RESET}")
            for admin in list(self.discovered['admin_panels'])[:5]:
                shock_factors.append(f"       → {admin}")
        
        if self.discovered['backup_files']:
            shock_factors.append(f"  {Colors.RED}[!!!] EXPOSED BACKUP FILES: {len(self.discovered['backup_files'])}{Colors.RESET}")
            for backup in list(self.discovered['backup_files'])[:5]:
                shock_factors.append(f"       → {backup}")
        
        if self.discovered['s3_buckets']:
            shock_factors.append(f"  {Colors.RED}[!!!] EXPOSED S3 BUCKETS: {len(self.discovered['s3_buckets'])}{Colors.RESET}")
            for bucket in list(self.discovered['s3_buckets'])[:5]:
                shock_factors.append(f"       → {bucket}")
        
        if self.discovered['graphql_endpoints']:
            shock_factors.append(f"  {Colors.RED}[!!!] GRAPHQL ENDPOINTS (Introspection risk): {len(self.discovered['graphql_endpoints'])}{Colors.RESET}")
        
        if self.discovered['emails']:
            shock_factors.append(f"  {Colors.YELLOW}[!] EMAIL ADDRESSES FOUND: {len(self.discovered['emails'])}{Colors.RESET}")
            for email in list(self.discovered['emails'])[:10]:
                shock_factors.append(f"       → {email}")
        
        if self.discovered['subdomains']:
            shock_factors.append(f"  {Colors.YELLOW}[!] SUBDOMAINS DISCOVERED: {len(self.discovered['subdomains'])}{Colors.RESET}")
            for sub in list(self.discovered['subdomains'])[:10]:
                shock_factors.append(f"       → {sub}")
        
        if self.discovered['api_endpoints']:
            shock_factors.append(f"  {Colors.YELLOW}[!] API ENDPOINTS: {len(self.discovered['api_endpoints'])}{Colors.RESET}")
            for api in list(self.discovered['api_endpoints'])[:10]:
                shock_factors.append(f"       → {api}")
        
        if not shock_factors:
            shock_factors.append(f"  {Colors.GREEN}[✓] No critical findings - target appears secure{Colors.RESET}")
        
        for shock in shock_factors:
            print(shock)
        
        # Technology Stack
        if self.discovered['technologies']:
            print(f"\n  {Colors.CYAN}🔧 DETECTED TECHNOLOGIES{Colors.RESET}")
            print(f"  {'─'*66}")
            for category, techs in self.discovered['technologies'].items():
                if techs:
                    print(f"  {Colors.WHITE}• {category}: {', '.join(techs)}{Colors.RESET}")
        
        # Assets
        print(f"\n  {Colors.MAGENTA}📦 ASSETS DISCOVERED{Colors.RESET}")
        print(f"  {'─'*66}")
        print(f"  {Colors.WHITE}• JavaScript Files:  {len(self.discovered['js_files'])}{Colors.RESET}")
        print(f"  {Colors.WHITE}• CSS Files:         {len(self.discovered['css_files'])}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Images:            {len(self.discovered['images'])}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Documents:         {len(self.discovered['documents'])}{Colors.RESET}")
        print(f"  {Colors.WHITE}• Archives:          {len(self.discovered['archives'])}{Colors.RESET}")
        
        # Parameters
        if self.discovered['parameters']:
            print(f"\n  {Colors.YELLOW}📝 URL PARAMETERS{Colors.RESET}")
            print(f"  {'─'*66}")
            for param in list(self.discovered['parameters'])[:20]:
                print(f"  {Colors.WHITE}• {param}{Colors.RESET}")
        
        # Comments with TODOs
        if self.discovered['comments']:
            print(f"\n  {Colors.MAGENTA}💬 INTERESTING COMMENTS{Colors.RESET}")
            print(f"  {'─'*66}")
            for comment in self.discovered['comments'][:10]:
                print(f"  {Colors.WHITE}• {comment['content'][:100]}...{Colors.RESET}")
        
        # Headers Analysis
        print(f"\n  {Colors.CYAN}🛡️ SECURITY HEADERS{Colors.RESET}")
        print(f"  {'─'*66}")
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME Sniffing',
            'Referrer-Policy': 'Referrer Policy',
        }
        
        for header, name in security_headers.items():
            if header in self.discovered['headers']:
                print(f"  {Colors.GREEN}✓ {name}: Present{Colors.RESET}")
            else:
                print(f"  {Colors.RED}✗ {name}: Missing{Colors.RESET}")
        
        # Save results
        self.save_results()
        
        # Final alert
        if self.discovered['config_files'] or self.discovered['admin_panels'] or self.discovered['backup_files']:
            print(f"\n  {Colors.RED}{Colors.BLINK}{'█'*70}{Colors.RESET}")
            print(f"  {Colors.RED}{Colors.BLINK}🚨 CRITICAL SECURITY ISSUES DETECTED - IMMEDIATE ACTION REQUIRED 🚨{Colors.RESET}")
            print(f"  {Colors.RED}{Colors.BLINK}{'█'*70}{Colors.RESET}")
        
        print(f"\n  {Colors.GREEN}✓ Full report saved: quantum_spider_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json{Colors.RESET}")
        print(f"  {Colors.GREEN}✓ Results saved: spider_results_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt{Colors.RESET}")
        print(f"  {Colors.CYAN}{'═'*70}{Colors.RESET}\n")
    
    def save_results(self):
        """Save results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON report
        json_report = {
            'target': self.target,
            'domain': self.domain,
            'scan_time': timestamp,
            'duration': time.time() - self.start_time,
            'statistics': self.stats,
            'discovered': {
                'urls': list(self.discovered['urls']),
                'internal_links': list(self.discovered['internal']),
                'external_links': list(self.discovered['external']),
                'admin_panels': list(self.discovered['admin_panels']),
                'login_panels': list(self.discovered['login_panels']),
                'api_endpoints': list(self.discovered['api_endpoints']),
                'graphql_endpoints': list(self.discovered['graphql_endpoints']),
                'config_files': list(self.discovered['config_files']),
                'backup_files': list(self.discovered['backup_files']),
                'subdomains': list(self.discovered['subdomains']),
                'emails': list(self.discovered['emails']),
                's3_buckets': list(self.discovered['s3_buckets']),
                'technologies': {k: list(v) for k, v in self.discovered['technologies'].items()},
                'js_files': list(self.discovered['js_files']),
                'css_files': list(self.discovered['css_files']),
                'images': list(self.discovered['images']),
                'documents': list(self.discovered['documents']),
            }
        }
        
        with open(f'quantum_spider_{self.domain}_{timestamp}.json', 'w') as f:
            json.dump(json_report, f, indent=2)
        
        # Text report
        with open(f'spider_results_{self.domain}_{timestamp}.txt', 'w') as f:
            f.write(f"XOPHY Quantum Spider Report - {self.target}\n")
            f.write(f"{'='*70}\n\n")
            
            f.write("CRITICAL FINDINGS:\n")
            f.write(f"{'-'*40}\n")
            if self.discovered['config_files']:
                f.write(f"Exposed Config Files: {len(self.discovered['config_files'])}\n")
                for cfg in self.discovered['config_files']:
                    f.write(f"  - {cfg}\n")
            
            if self.discovered['admin_panels']:
                f.write(f"\nAdmin Panels: {len(self.discovered['admin_panels'])}\n")
                for admin in self.discovered['admin_panels']:
                    f.write(f"  - {admin}\n")
            
            f.write(f"\nEmails: {len(self.discovered['emails'])}\n")
            for email in self.discovered['emails']:
                f.write(f"  - {email}\n")
            
            f.write(f"\nSubdomains: {len(self.discovered['subdomains'])}\n")
            for sub in self.discovered['subdomains']:
                f.write(f"  - {sub}\n")
            
            f.write(f"\nAPI Endpoints: {len(self.discovered['api_endpoints'])}\n")
            for api in self.discovered['api_endpoints']:
                f.write(f"  - {api}\n")
    
    def run(self):
        """Main execution"""
        print(f"\n  {Colors.RED}{Colors.BOLD}{'█'*70}{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}║          🕷️ XOPHY QUANTUM SPIDER v3.0 - NEXT-GEN RECONNAISSANCE          ║{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}║                    [ DEEP WEB | DARK WEB | SURFACE ]                    ║{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}{'█'*70}{Colors.RESET}")
        
        print(f"\n  {Colors.CYAN}[*] Target: {self.target}{Colors.RESET}")
        print(f"  {Colors.CYAN}[*] Domain: {self.domain}{Colors.RESET}")
        print(f"  {Colors.CYAN}[*] Max Depth: {self.max_depth} | Max Pages: {self.max_pages} | Threads: {self.threads}{Colors.RESET}")
        print(f"\n  {Colors.GREEN}[*] Starting quantum spider...{Colors.RESET}\n")
        
        self.start_time = time.time()
        
        # Start crawling threads
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.crawl_worker) for _ in range(self.threads)]
            for future in as_completed(futures):
                pass
        
        # Fuzz for hidden endpoints
        self.fuzz_endpoints()
        
        # Generate shocking report
        self.generate_shocking_report()


def run(target, max_depth=5, max_pages=500, threads=50):
    """Wrapper function for CLI compatibility"""
    spider = QuantumSpider(target, max_depth, max_pages, threads)
    spider.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(f"{Colors.CYAN}◎ Enter target domain/IP → {Colors.RESET}")
    
    run(target)
