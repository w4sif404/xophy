#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║         XOPHY QUANTUM SPIDER v3.0 - ULTIMATE RECONNAISSANCE ENGINE            ║
║              [ AI-POWERED | ZERO-DAY DISCOVERY | EXPLOIT READY ]              ║
║                         ⚡ Enterprise Grade Security Tool ⚡                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import re
import urllib3
import json
import time
import hashlib
import random
import threading
import queue
import warnings
from urllib.parse import urlparse, urljoin, parse_qs
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field, asdict
import os
import sys

# Suppress BeautifulSoup XML warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ──────────────────────────────────────────────────────────────────────────────
# ULTIMATE COLOR SCHEME
# ──────────────────────────────────────────────────────────────────────────────

class Colors:
    # Base colors
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    RESET = '\033[0m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BLACK = '\033[40m'

@dataclass
class Vulnerability:
    name: str
    severity: str
    endpoint: str
    description: str
    proof: str
    remediation: str
    cvss_score: float
    exploit_available: bool = False
    exploit_command: str = ""

class QuantumSpiderUltimate:
    """Ultimate Web Spider with Enterprise-Grade Discovery"""
    
    def __init__(self, target: str, max_depth: int = 5, max_pages: int = 500, threads: int = 50):
        self.target = target if target.startswith(('http://', 'https://')) else f'https://{target}'
        self.domain = urlparse(self.target).netloc
        self.base_domain = self.domain.replace('www.', '')
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.threads = threads
        self.start_time = None
        
        # Session with advanced headers
        self.session = self._create_session()
        
        # Comprehensive data storage
        self.data = {
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
            'vulnerabilities': [],
            'attack_vectors': [],
            'exposed_secrets': [],
            'interesting_paths': set(),
        }
        
        self.visited = set()
        self.to_visit = queue.Queue()
        self.to_visit.put((self.target, 0))
        self.lock = threading.Lock()
        
        self.stats = {
            'requests': 0,
            'success': 0,
            'errors': 0,
            'redirects': 0,
            'data_transferred': 0,
        }
        
        # Expanded wordlists
        self.wordlists = self._load_wordlists()
    
    def _create_session(self) -> requests.Session:
        """Create advanced session with rotating headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        })
        return session
    
    def _load_wordlists(self) -> Dict:
        """Load comprehensive wordlists"""
        return {
            'admin_paths': [
                'admin', 'administrator', 'adminpanel', 'cp', 'cpanel', 'webadmin',
                'dashboard', 'controlpanel', 'manage', 'operator', 'sysadmin',
                'admin123', 'adminarea', 'adm', 'backend', 'moderator'
            ],
            'api_paths': [
                'api', 'v1', 'v2', 'v3', 'v4', 'rest', 'graphql', 'swagger',
                'openapi', 'docs', 'apidocs', 'api-docs', 'redoc', 'json',
                'data', 'service', 'services', 'ws', 'websocket', 'rpc'
            ],
            'sensitive_dirs': [
                '.git', '.svn', '.hg', '.env', 'backup', 'temp', 'tmp',
                'logs', 'debug', 'test', 'dev', 'staging', 'private',
                'secret', 'hidden', 'internal', 'conf', 'config', 'backups'
            ],
            'backup_extensions': [
                '.bak', '.old', '.backup', '~', '.swp', '.swo', '.save',
                '.orig', '.sql', '.dump', '.tar', '.gz', '.zip', '.7z',
                '.rar', '.tgz', '.bz2', '.xz', '.001'
            ],
            'config_files': [
                '.env', '.env.local', '.env.production', '.env.development',
                '.git/config', '.aws/credentials', '.ssh/id_rsa',
                'wp-config.php', 'config.php', 'database.yml', 'secrets.yml',
                'credentials.json', 'service-account.json', '.htpasswd',
                '.htaccess', 'robots.txt', 'sitemap.xml', 'crossdomain.xml'
            ],
            'sensitive_patterns': {
                'api_keys': r'(api[_-]?key|apikey|access[_-]?key|secret[_-]?key)[\s]*[:=][\s]*["\']?([a-zA-Z0-9]{16,64})',
                'aws_keys': r'AKIA[0-9A-Z]{16}',
                'jwt_tokens': r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
                'passwords': r'(password|passwd|pwd)[\s]*[:=][\s]*["\']?([^"\'\s]{6,})',
                'database_urls': r'(mysql|postgresql|mongodb|redis|elasticsearch)://[^\s"\']+',
                'slack_webhooks': r'https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[a-zA-Z0-9]+',
                'github_tokens': r'gh[psu]_[a-zA-Z0-9]{36}',
                'private_keys': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
            }
        }
    
    def fetch_url(self, url: str, depth: int) -> Optional[Tuple[requests.Response, int]]:
        """Fetch URL with advanced error handling"""
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=15, verify=False, allow_redirects=True)
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
        except:
            with self.lock:
                self.stats['errors'] += 1
            return None, depth
    
    def extract_all_links(self, html: str, base_url: str) -> Set[str]:
        """Extract all links from HTML - FIXED for XML warning"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        # Extract from tags
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'form']):
            attr = tag.get('href') or tag.get('src') or tag.get('action')
            if attr:
                full_url = urljoin(base_url, attr)
                if full_url.startswith(('http://', 'https://')):
                    links.add(full_url)
        
        return links
    
    def analyze_page(self, url: str, response: requests.Response, depth: int):
        """Comprehensive page analysis - FIXED for XML warning"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Technology Detection
        html_lower = response.text.lower()
        tech_map = {
            'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
            'Apache': ['apache', 'Apache'],
            'Nginx': ['nginx', 'Nginx'],
            'IIS': ['iis', 'IIS'],
            'React': ['react', '_reactRoot', 'ReactDOM'],
            'Vue.js': ['vue', 'data-v-', 'Vue'],
            'Angular': ['ng-', 'ng-app', 'Angular'],
            'jQuery': ['jquery', 'jQuery'],
            'Bootstrap': ['bootstrap', 'Bootstrap'],
            'Font Awesome': ['fontawesome', 'font-awesome'],
            'Google Analytics': ['google-analytics', 'gtag'],
            'Facebook Pixel': ['facebook.com/tr', 'fbq'],
        }
        
        for tech, indicators in tech_map.items():
            if any(ind in html_lower for ind in indicators):
                self.data['technologies']['Detected'].add(tech)
        
        # Extract Emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = set(re.findall(email_pattern, response.text))
        emails = {e for e in emails if not e.endswith(('.png', '.jpg', '.gif', '.css', '.js', '.svg'))}
        self.data['emails'].update(emails)
        
        # Extract IPs
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = set(re.findall(ip_pattern, response.text))
        self.data['ip_addresses'].update(ips)
        
        # Extract Phone Numbers
        phone_pattern = r'\+?[\d\s\-\(\)]{10,20}'
        phones = set(re.findall(phone_pattern, response.text))
        self.data['phone_numbers'].update([p for p in phones if len(p) > 8])
        
        # Extract API Endpoints
        api_patterns = [
            r'/(?:api|v\d+|rest|graphql)/[^\s"\']+',
            r'"/wp-json/wp/v2/[^"]+"',
            r"['\"]/?(?:api|rest|graphql)/[a-zA-Z0-9\-_/]+['\"]",
        ]
        for pattern in api_patterns:
            matches = re.findall(pattern, response.text, re.I)
            for match in matches:
                full_url = urljoin(url, match)
                self.data['api_endpoints'].add(full_url)
        
        # GraphQL Detection
        if 'graphql' in response.text.lower() or '__schema' in response.text:
            self.data['graphql_endpoints'].add(url)
        
        # Admin Panel Detection
        admin_keywords = ['admin', 'cpanel', 'dashboard', 'wp-admin', 'administrator']
        for keyword in admin_keywords:
            if keyword in url.lower():
                self.data['admin_panels'].add(url)
        
        # Extract Assets
        for script in soup.find_all('script', src=True):
            self.data['js_files'].add(urljoin(url, script['src']))
        
        for link in soup.find_all('link', rel='stylesheet'):
            if link.get('href'):
                self.data['css_files'].add(urljoin(url, link['href']))
        
        for img in soup.find_all('img', src=True):
            self.data['images'].add(urljoin(url, img['src']))
        
        # Documents
        doc_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']
        for link in soup.find_all('a', href=True):
            if any(link['href'].lower().endswith(ext) for ext in doc_extensions):
                self.data['documents'].add(urljoin(url, link['href']))
        
        # Extract Comments (TODOs, FIXMEs)
        comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text)
        for comment in comments:
            if re.search(r'TODO|FIXME|HACK|SECURITY|PASSWORD|API_KEY|BUG', comment, re.I):
                self.data['comments'].append({
                    'url': url,
                    'content': comment.strip()[:200]
                })
        
        # Extract Subdomains
        subdomain_pattern = rf'([a-zA-Z0-9_-]+)\.{re.escape(self.base_domain)}'
        subdomains = set(re.findall(subdomain_pattern, response.text, re.I))
        for sub in subdomains:
            self.data['subdomains'].add(f"{sub}.{self.base_domain}")
        
        # Extract Parameters
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            self.data['parameters'].update(params.keys())
        
        # Extract Headers
        for header, value in response.headers.items():
            self.data['headers'][header].append(value)
        
        # Extract Cookies
        for cookie in response.cookies:
            self.data['cookies'].add(f"{cookie.name}={cookie.value}")
    
    def fuzz_endpoints(self):
        """Fuzz for hidden endpoints"""
        print(f"\n  {Colors.CYAN}{Colors.BOLD}[*] Fuzzing for hidden endpoints...{Colors.RESET}")
        
        # Test admin paths
        for path in self.wordlists['admin_paths']:
            url = f"{self.target}/{path}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    self.data['admin_panels'].add(url)
                    print(f"    {Colors.GREEN}[+] Found: {url}{Colors.RESET}")
                elif resp.status_code in [401, 403]:
                    self.data['admin_panels'].add(f"{url} (Protected)")
                    print(f"    {Colors.YELLOW}[!] Protected: {url}{Colors.RESET}")
            except:
                pass
        
        # Test API paths
        for path in self.wordlists['api_paths']:
            url = f"{self.target}/{path}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    self.data['api_endpoints'].add(url)
                    print(f"    {Colors.GREEN}[+] API: {url}{Colors.RESET}")
            except:
                pass
        
        # Test sensitive directories
        for path in self.wordlists['sensitive_dirs']:
            url = f"{self.target}/{path}"
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    self.data['interesting_paths'].add(url)
                    print(f"    {Colors.RED}[!] Sensitive: {url}{Colors.RESET}")
            except:
                pass
    
    def check_vulnerabilities(self):
        """Check for vulnerabilities"""
        print(f"\n  {Colors.RED}{Colors.BOLD}[*] Scanning for vulnerabilities...{Colors.RESET}")
        
        # Check backup files
        for path in self.wordlists['backup_extensions']:
            for base in ['', '/admin', '/wp-admin', '/backup', '/~']:
                test_url = f"{self.target}{base}{path}"
                try:
                    resp = self.session.get(test_url, timeout=3)
                    if resp.status_code == 200 and len(resp.content) > 100:
                        self.data['backup_files'].add(test_url)
                        self.data['vulnerabilities'].append(Vulnerability(
                            name="Exposed Backup File",
                            severity="HIGH",
                            endpoint=test_url,
                            description=f"Backup file accessible ({len(resp.content)} bytes)",
                            proof=f"File contains {len(resp.content)} bytes of data",
                            remediation="Remove backup files from webroot immediately",
                            cvss_score=7.5,
                            exploit_available=True,
                            exploit_command=f"wget {test_url} && strings {test_url.split('/')[-1]} | grep -E 'password|secret|key'"
                        ))
                        print(f"    {Colors.RED}[!!!] Backup found: {test_url}{Colors.RESET}")
                except:
                    pass
        
        # Check config files
        for config in self.wordlists['config_files']:
            test_url = f"{self.target}/{config}"
            try:
                resp = self.session.get(test_url, timeout=3)
                if resp.status_code == 200:
                    self.data['config_files'].add(test_url)
                    self.data['vulnerabilities'].append(Vulnerability(
                        name="Exposed Configuration File",
                        severity="CRITICAL",
                        endpoint=test_url,
                        description="Configuration file exposed",
                        proof="File contains sensitive configuration data",
                        remediation="Move configuration files outside webroot, restrict access",
                        cvss_score=9.0,
                        exploit_available=True,
                        exploit_command=f"curl {test_url} | grep -E 'DB_|PASSWORD|SECRET|API'"
                    ))
                    print(f"    {Colors.RED}[!!!] Config exposed: {test_url}{Colors.RESET}")
            except:
                pass
        
        # Check for exposed secrets in source
        for pattern_name, pattern in self.wordlists['sensitive_patterns'].items():
            for url in list(self.data['urls'])[:20]:
                try:
                    resp = self.session.get(url, timeout=5)
                    matches = re.findall(pattern, resp.text, re.I)
                    if matches:
                        self.data['exposed_secrets'].append({
                            'type': pattern_name,
                            'value': str(matches[0])[:50],
                            'url': url
                        })
                        print(f"    {Colors.RED}[!!!] Exposed {pattern_name} in {url}{Colors.RESET}")
                except:
                    pass
    
    def generate_attack_paths(self):
        """Generate attack vectors"""
        print(f"\n  {Colors.MAGENTA}{Colors.BOLD}[*] Generating attack vectors...{Colors.RESET}")
        
        attack_paths = []
        
        # Admin brute force
        for admin in list(self.data['admin_panels'])[:5]:
            attack_paths.append({
                'name': 'Admin Panel Brute Force',
                'target': admin,
                'tool': 'hydra',
                'command': f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {self.domain} http-post-form \"{admin}:username=^USER^&password=^PASS^:F=Invalid\"",
                'risk': 'CRITICAL',
                'time_estimate': '2-24 hours',
                'priority': 1
            })
            print(f"    {Colors.RED}[!] Attack Vector: Brute force {admin}{Colors.RESET}")
        
        # API enumeration
        for api in list(self.data['api_endpoints'])[:5]:
            attack_paths.append({
                'name': 'API Enumeration',
                'target': api,
                'tool': 'curl',
                'command': f'curl -X GET "{api}" -H "X-API-Key: test" -H "Authorization: Bearer test"',
                'risk': 'HIGH',
                'time_estimate': 'Minutes',
                'priority': 2
            })
            print(f"    {Colors.YELLOW}[!] Attack Vector: API enumeration on {api}{Colors.RESET}")
        
        # Backup extraction
        if self.data['backup_files']:
            attack_paths.append({
                'name': 'Credential Extraction from Backups',
                'target': list(self.data['backup_files'])[0],
                'tool': 'wget/strings',
                'command': f"wget {list(self.data['backup_files'])[0]} && strings {list(self.data['backup_files'])[0].split('/')[-1]} | grep -E 'password|secret|key|token'",
                'risk': 'CRITICAL',
                'time_estimate': '5 minutes',
                'priority': 1
            })
            print(f"    {Colors.RED}[!] Attack Vector: Extract credentials from backups{Colors.RESET}")
        
        self.data['attack_vectors'] = attack_paths
        return attack_paths
    
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
                self.data['urls'].add(url)
            
            result = self.fetch_url(url, depth)
            if not result:
                continue
            
            response, current_depth = result
            
            if response.status_code == 200:
                self.analyze_page(url, response, current_depth)
                
                if current_depth < self.max_depth:
                    links = self.extract_all_links(response.text, url)
                    for link in links:
                        parsed = urlparse(link)
                        if parsed.netloc == self.domain or not parsed.netloc:
                            if link not in self.visited:
                                with self.lock:
                                    self.data['internal'].add(link)
                                self.to_visit.put((link, current_depth + 1))
                        else:
                            with self.lock:
                                self.data['external'].add(link)
                
                with self.lock:
                    if len(self.visited) % 10 == 0:
                        print(f"  {Colors.CYAN}[*] Crawled: {len(self.visited)}/{self.max_pages} | Found: {len(self.data['internal'])} links | Depth: {current_depth}{Colors.RESET}")
    
    def generate_ultimate_report(self):
        """Generate ultimate clear report"""
        elapsed = time.time() - self.start_time
        
        # Calculate risk score
        risk_score = min(
            len(self.data['vulnerabilities']) * 15 +
            len(self.data['admin_panels']) * 10 +
            len(self.data['backup_files']) * 20 +
            len(self.data['config_files']) * 25, 100
        )
        
        risk_level = "CRITICAL" if risk_score >= 70 else "HIGH" if risk_score >= 50 else "MEDIUM" if risk_score >= 30 else "LOW"
        risk_color = Colors.RED if risk_level == "CRITICAL" else Colors.YELLOW if risk_level == "HIGH" else Colors.CYAN
        
        # Header
        print(f"\n\n  {Colors.RED}{Colors.BOLD}{'█'*80}{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}║                    🕷️ XOPHY QUANTUM SPIDER v5.0 - ULTIMATE REPORT                    ║{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}{'█'*80}{Colors.RESET}")
        
        # SECTION 1: EXECUTIVE SUMMARY
        print(f"\n  {Colors.CYAN}{Colors.BOLD}📋 EXECUTIVE SUMMARY{Colors.RESET}")
        print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
        print(f"  {Colors.WHITE}Target:        {self.target}{Colors.RESET}")
        print(f"  {Colors.WHITE}Scan Duration: {elapsed:.2f} seconds ({elapsed/60:.1f} minutes){Colors.RESET}")
        print(f"  {Colors.WHITE}Pages Crawled: {len(self.visited)}/{self.max_pages}{Colors.RESET}")
        print(f"  {Colors.WHITE}Data Transfer: {self.stats['data_transferred'] / 1024 / 1024:.2f} MB{Colors.RESET}")
        print(f"  {Colors.WHITE}Requests:      {self.stats['requests']} (Success: {self.stats['success']}, Errors: {self.stats['errors']}){Colors.RESET}")
        print(f"  {risk_color}Risk Score:    {risk_score}/100 ({risk_level}){Colors.RESET}")
        
        # SECTION 2: CRITICAL FINDINGS
        print(f"\n  {Colors.RED}{Colors.BOLD}{Colors.BLINK}⚠️ CRITICAL FINDINGS - ACT IMMEDIATELY ⚠️{Colors.RESET}")
        print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
        
        critical_found = False
        
        if self.data['config_files']:
            critical_found = True
            print(f"  {Colors.RED}{Colors.BOLD}[✓] CONFIGURATION FILES EXPOSED: {len(self.data['config_files'])}{Colors.RESET}")
            for cfg in list(self.data['config_files'])[:5]:
                print(f"      {Colors.RED}→ {cfg}{Colors.RESET}")
        
        if self.data['backup_files']:
            critical_found = True
            print(f"  {Colors.RED}{Colors.BOLD}[✓] BACKUP FILES EXPOSED: {len(self.data['backup_files'])}{Colors.RESET}")
            for bkp in list(self.data['backup_files'])[:5]:
                print(f"      {Colors.RED}→ {bkp}{Colors.RESET}")
        
        if self.data['admin_panels']:
            critical_found = True
            print(f"  {Colors.YELLOW}{Colors.BOLD}[✓] ADMIN PANELS EXPOSED: {len(self.data['admin_panels'])}{Colors.RESET}")
            for admin in list(self.data['admin_panels'])[:5]:
                print(f"      {Colors.YELLOW}→ {admin}{Colors.RESET}")
        
        if self.data['exposed_secrets']:
            critical_found = True
            print(f"  {Colors.RED}{Colors.BOLD}[✓] EXPOSED SECRETS: {len(self.data['exposed_secrets'])}{Colors.RESET}")
            for secret in self.data['exposed_secrets'][:3]:
                print(f"      {Colors.RED}→ {secret['type']}: {secret['value']}{Colors.RESET}")
        
        if not critical_found:
            print(f"  {Colors.GREEN}[✓] No critical findings detected{Colors.RESET}")
        
        # SECTION 3: VULNERABILITIES
        if self.data['vulnerabilities']:
            print(f"\n  {Colors.RED}{Colors.BOLD}🔓 VULNERABILITIES DETECTED ({len(self.data['vulnerabilities'])}{Colors.RESET}")
            print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
            
            for vuln in self.data['vulnerabilities'][:10]:
                severity_color = Colors.RED if vuln.severity == "CRITICAL" else Colors.YELLOW
                print(f"  {severity_color}[!] {vuln.name} [{vuln.severity}] | CVSS: {vuln.cvss_score}{Colors.RESET}")
                print(f"      Endpoint: {vuln.endpoint[:70]}")
                print(f"      Fix: {vuln.remediation[:70]}")
                if vuln.exploit_available:
                    print(f"      Exploit: {vuln.exploit_command[:70]}...")
                print()
        
        # SECTION 4: ATTACK VECTORS
        if self.data['attack_vectors']:
            print(f"\n  {Colors.MAGENTA}{Colors.BOLD}🎯 ATTACK VECTORS (What Attackers Can Do){Colors.RESET}")
            print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
            
            for vector in self.data['attack_vectors'][:10]:
                risk_color = Colors.RED if vector['risk'] == "CRITICAL" else Colors.YELLOW
                print(f"  {risk_color}[→] {vector['name']} [{vector['risk']}] | Time: {vector['time_estimate']}{Colors.RESET}")
                print(f"      Target: {vector['target'][:60]}")
                print(f"      Command: {vector['command'][:70]}...")
                print()
        
        # SECTION 5: ASSETS SUMMARY
        print(f"\n  {Colors.CYAN}{Colors.BOLD}📦 EXPOSED ASSETS SUMMARY{Colors.RESET}")
        print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
        
        assets = [
            ("Admin Panels", len(self.data['admin_panels']), Colors.RED),
            ("Login Panels", len(self.data['login_panels']), Colors.YELLOW),
            ("API Endpoints", len(self.data['api_endpoints']), Colors.CYAN),
            ("GraphQL Endpoints", len(self.data['graphql_endpoints']), Colors.MAGENTA),
            ("Email Addresses", len(self.data['emails']), Colors.WHITE),
            ("Subdomains", len(self.data['subdomains']), Colors.GREEN),
            ("JavaScript Files", len(self.data['js_files']), Colors.WHITE),
            ("CSS Files", len(self.data['css_files']), Colors.WHITE),
            ("Images", len(self.data['images']), Colors.WHITE),
            ("Documents", len(self.data['documents']), Colors.WHITE),
            ("IP Addresses", len(self.data['ip_addresses']), Colors.DIM),
        ]
        
        for name, count, color in assets:
            if count > 0:
                print(f"  {color}• {name}: {count:,}{Colors.RESET}")
        
        # SECTION 6: EMAILS (For OSINT)
        if self.data['emails']:
            print(f"\n  {Colors.CYAN}{Colors.BOLD}📧 DISCOVERED EMAIL ADDRESSES ({len(self.data['emails'])}){Colors.RESET}")
            print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
            for email in list(self.data['emails'])[:15]:
                print(f"  {Colors.WHITE}• {email}{Colors.RESET}")
            if len(self.data['emails']) > 15:
                print(f"  {Colors.DIM}... and {len(self.data['emails']) - 15} more{Colors.RESET}")
        
        # SECTION 7: SUBDOMAINS
        if self.data['subdomains']:
            print(f"\n  {Colors.GREEN}{Colors.BOLD}🌐 DISCOVERED SUBDOMAINS ({len(self.data['subdomains'])}){Colors.RESET}")
            print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
            for sub in list(self.data['subdomains'])[:10]:
                print(f"  {Colors.WHITE}• {sub}{Colors.RESET}")
        
        # SECTION 8: TECHNOLOGY STACK
        if self.data['technologies']:
            print(f"\n  {Colors.CYAN}{Colors.BOLD}🔧 TECHNOLOGY STACK{Colors.RESET}")
            print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
            for tech in sorted(self.data['technologies']['Detected']):
                print(f"  {Colors.WHITE}• {tech}{Colors.RESET}")
        
        # SECTION 9: SECURITY HEADERS
        print(f"\n  {Colors.YELLOW}{Colors.BOLD}🛡️ SECURITY HEADERS STATUS{Colors.RESET}")
        print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS (Prevents SSL stripping)',
            'Content-Security-Policy': 'CSP (Prevents XSS)',
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME Sniffing Protection',
            'Referrer-Policy': 'Referrer Policy',
            'X-XSS-Protection': 'XSS Protection',
        }
        
        for header, description in security_headers.items():
            if header in self.data['headers']:
                print(f"  {Colors.GREEN}✓ {description}: Present{Colors.RESET}")
            else:
                print(f"  {Colors.RED}✗ {description}: MISSING{Colors.RESET}")
        
        # SECTION 10: REMEDIATION STEPS
        print(f"\n  {Colors.GREEN}{Colors.BOLD}🔧 IMMEDIATE REMEDIATION STEPS{Colors.RESET}")
        print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
        
        remediation_steps = []
        step_num = 1
        
        if self.data['backup_files']:
            remediation_steps.append(f"{step_num}. Remove all exposed backup files immediately")
            step_num += 1
            remediation_steps.append(f"{step_num}. Configure .gitignore to exclude backup files")
            step_num += 1
        
        if self.data['config_files']:
            remediation_steps.append(f"{step_num}. Move configuration files outside webroot")
            step_num += 1
            remediation_steps.append(f"{step_num}. Rotate any exposed credentials immediately")
            step_num += 1
        
        if self.data['admin_panels']:
            remediation_steps.append(f"{step_num}. Implement IP whitelisting for admin panels")
            step_num += 1
            remediation_steps.append(f"{step_num}. Enable Multi-Factor Authentication (MFA)")
            step_num += 1
        
        if 'Strict-Transport-Security' not in self.data['headers']:
            remediation_steps.append(f"{step_num}. Enable HSTS header")
            step_num += 1
        
        if 'Content-Security-Policy' not in self.data['headers']:
            remediation_steps.append(f"{step_num}. Implement Content Security Policy (CSP)")
            step_num += 1
        
        if not remediation_steps:
            remediation_steps.append("✓ No immediate remediation required")
        
        for step in remediation_steps[:12]:
            print(f"  {Colors.WHITE}{step}{Colors.RESET}")
        
        # SECTION 11: FILES SAVED
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f'quantum_spider_{self.domain}_{timestamp}.json'
        txt_file = f'spider_results_{self.domain}_{timestamp}.txt'
        
        print(f"\n  {Colors.CYAN}{Colors.BOLD}📁 REPORT FILES SAVED{Colors.RESET}")
        print(f"  {Colors.DIM}{'─'*76}{Colors.RESET}")
        print(f"  {Colors.GREEN}✓ JSON Report: {json_file}{Colors.RESET}")
        print(f"  {Colors.GREEN}✓ Text Report: {txt_file}{Colors.RESET}")
        
        # FINAL WARNING
        if critical_found:
            print(f"\n  {Colors.RED}{Colors.BLINK}{'█'*80}{Colors.RESET}")
            print(f"  {Colors.RED}{Colors.BLINK}🚨 CRITICAL SECURITY ISSUES FOUND - IMMEDIATE ACTION REQUIRED 🚨{Colors.RESET}")
            print(f"  {Colors.RED}{Colors.BLINK}{'█'*80}{Colors.RESET}")
        
        print(f"\n  {Colors.CYAN}{'═'*80}{Colors.RESET}\n")
        
        # Save files
        self.save_results(json_file, txt_file)
    
    def save_results(self, json_file: str, txt_file: str):
        """Save results to files"""
        report_data = {
            'target': self.target,
            'domain': self.domain,
            'scan_time': datetime.now().isoformat(),
            'duration': time.time() - self.start_time,
            'statistics': self.stats,
            'risk_score': min(
                len(self.data['vulnerabilities']) * 15 +
                len(self.data['admin_panels']) * 10 +
                len(self.data['backup_files']) * 20, 100
            ),
            'critical_findings': {
                'admin_panels': list(self.data['admin_panels']),
                'backup_files': list(self.data['backup_files']),
                'config_files': list(self.data['config_files']),
                'exposed_secrets': self.data['exposed_secrets'],
            },
            'vulnerabilities': [
                {'name': v.name, 'severity': v.severity, 'endpoint': v.endpoint, 'cvss': v.cvss_score}
                for v in self.data['vulnerabilities']
            ],
            'attack_vectors': self.data['attack_vectors'],
            'emails': list(self.data['emails']),
            'subdomains': list(self.data['subdomains']),
            'technologies': list(self.data['technologies']['Detected']),
            'api_endpoints': list(self.data['api_endpoints']),
            'statistics': {
                'pages_crawled': len(self.visited),
                'internal_links': len(self.data['internal']),
                'external_links': len(self.data['external']),
                'js_files': len(self.data['js_files']),
                'css_files': len(self.data['css_files']),
                'images': len(self.data['images']),
                'documents': len(self.data['documents']),
            }
        }
        
        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Text report
        with open(txt_file, 'w') as f:
            f.write(f"XOPHY Quantum Spider Report - {self.target}\n")
            f.write(f"{'='*70}\n\n")
            f.write("CRITICAL FINDINGS:\n")
            f.write(f"{'-'*40}\n")
            
            if self.data['config_files']:
                f.write(f"Exposed Config Files: {len(self.data['config_files'])}\n")
                for cfg in self.data['config_files']:
                    f.write(f"  - {cfg}\n")
            
            if self.data['backup_files']:
                f.write(f"\nExposed Backup Files: {len(self.data['backup_files'])}\n")
                for bkp in self.data['backup_files']:
                    f.write(f"  - {bkp}\n")
            
            if self.data['admin_panels']:
                f.write(f"\nAdmin Panels: {len(self.data['admin_panels'])}\n")
                for admin in self.data['admin_panels']:
                    f.write(f"  - {admin}\n")
            
            f.write(f"\nEmails: {len(self.data['emails'])}\n")
            for email in self.data['emails']:
                f.write(f"  - {email}\n")
    
    def run(self):
        """Main execution"""
        print(f"\n  {Colors.RED}{Colors.BOLD}{'█'*80}{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}║          🕷️ XOPHY QUANTUM SPIDER v5.0 - ULTIMATE RECONNAISSANCE           ║{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}║                    [ ENTERPRISE | AI-POWERED | EXPLOIT READY ]                    ║{Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}{'█'*80}{Colors.RESET}")
        
        print(f"\n  {Colors.CYAN}[*] Target: {self.target}{Colors.RESET}")
        print(f"  {Colors.CYAN}[*] Domain: {self.domain}{Colors.RESET}")
        print(f"  {Colors.CYAN}[*] Max Depth: {self.max_depth} | Max Pages: {self.max_pages} | Threads: {self.threads}{Colors.RESET}")
        print(f"\n  {Colors.GREEN}[*] Starting quantum spider...{Colors.RESET}\n")
        
        self.start_time = time.time()
        
        # Start crawling
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.crawl_worker) for _ in range(self.threads)]
            for future in as_completed(futures):
                pass
        
        # Post-processing
        self.fuzz_endpoints()
        self.check_vulnerabilities()
        self.generate_attack_paths()
        self.generate_ultimate_report()


def run(target, max_depth=5, max_pages=500, threads=50):
    """Wrapper function"""
    spider = QuantumSpiderUltimate(target, max_depth, max_pages, threads)
    spider.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(f"{Colors.CYAN}◎ Enter target domain/IP → {Colors.RESET}")
    
    run(target)
