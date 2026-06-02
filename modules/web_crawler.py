#!/usr/bin/env python3
"""
Xophy Elite Web Crawler - Ultimate Edition
Combines speed of original with advanced features
"""

import requests
import re
import urllib3
import time
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter
import sys
import json
from datetime import datetime
import threading

# Suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'

def run(target_url, max_pages=200, threads=30):
    """Main web crawler - Optimized for maximum email extraction"""
    
    print(f"\n{Colors.CYAN}{'━'*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}  🕷️  XOPHY ELITE - ULTIMATE EMAIL HARVESTER{Colors.END}")
    print(f"{Colors.CYAN}{'━'*70}{Colors.END}")
    print(f"{Colors.BOLD}  Target: {target_url}{Colors.END}")
    print(f"{Colors.CYAN}{'━'*70}{Colors.END}\n")
    
    # Normalize URL
    if not target_url.startswith(('http://', 'https://')):
        target_url = f"https://{target_url}"
    
    domain = urlparse(target_url).netloc
    
    # Results storage
    results = {
        'urls': set(),
        'internal_links': set(),
        'external_links': set(),
        'js_files': set(),
        'css_files': set(),
        'images': set(),
        'documents': set(),
        'emails': set(),
        'emails_with_context': [],
        'subdomains': set(),
        'api_endpoints': set(),
        'parameters': set(),
        'technologies': set(),
        'phone_numbers': set(),
        'social_links': set(),
        'forms': [],
        'comments': [],
        'status_codes': Counter(),
        'response_times': []
    }
    
    visited = set()
    to_visit = {target_url}
    
    # Session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    
    # Comprehensive email patterns
    def extract_all_emails(text, url):
        """Extract ALL emails using multiple patterns"""
        emails_found = set()
        
        # Pattern 1: Standard email
        pattern1 = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Pattern 2: Encoded emails (user[at]domain[dot]com)
        pattern2 = r'[a-zA-Z0-9._%+-]+\s*\[at\]\s*[a-zA-Z0-9.-]+\s*\[dot\]\s*[a-zA-Z]{2,}'
        
        # Pattern 3: Spaced emails (user @ domain . com)
        pattern3 = r'[a-zA-Z0-9._%+-]+\s+@\s+[a-zA-Z0-9.-]+\s+\.\s+[a-zA-Z]{2,}'
        
        # Pattern 4: HTML encoded
        pattern4 = r'[a-zA-Z0-9._%+-]+&#64;[a-zA-Z0-9.-]+&#46;[a-zA-Z]{2,}'
        
        # Pattern 5: Parenthesis encoded
        pattern5 = r'[a-zA-Z0-9._%+-]+\s*\(at\)\s*[a-zA-Z0-9.-]+\s*\(dot\)\s*[a-zA-Z]{2,}'
        
        all_patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]
        
        for pattern in all_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean the email
                email = match.lower()
                email = email.replace('[at]', '@').replace('[dot]', '.')
                email = email.replace('(at)', '@').replace('(dot)', '.')
                email = email.replace('&#64;', '@').replace('&#46;', '.')
                email = re.sub(r'\s+', '', email)
                
                # Filter out invalid
                if not any(x in email for x in ['.png', '.jpg', '.gif', '.svg', '.css', '.js', 'example.com']):
                    if '@' in email and '.' in email.split('@')[1] and len(email) < 100:
                        emails_found.add(email)
                        
                        # Get context for this email
                        idx = text.find(match)
                        context = text[max(0, idx-100):min(len(text), idx+200)].replace('\n', ' ').strip()
                        
                        results['emails_with_context'].append({
                            'email': email,
                            'source': url,
                            'context': context[:200]
                        })
        
        return emails_found
    
    def extract_phone_numbers(text):
        """Extract phone numbers - improved"""
        phones = set()
        
        # Pakistani phone number patterns
        patterns = [
            r'\+92[\d]{10}',  # +923xxxxxxxxx
            r'0[3-5][0-9]{9}',  # 03xxxxxxxxx
            r'\(?0[0-9]{2,4}\)?[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}',  # General format
            r'[0-9]{4}[-.\s][0-9]{7}',  # XXXX-XXXXXXX
            r'[0-9]{3}[-.\s][0-9]{4}[-.\s][0-9]{4}',  # XXX-XXXX-XXXX
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean the number
                cleaned = re.sub(r'[^\d+]', '', match)
                # Only keep valid length numbers (10-13 digits for Pakistani)
                if 10 <= len(cleaned) <= 13:
                    phones.add(cleaned)
        
        return phones
    
    def extract_links(html, base_url):
        """Extract all links from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'iframe']):
            url = tag.get('href') or tag.get('src')
            if not url:
                continue
            
            if url.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                continue
            
            full_url = urljoin(base_url, url)
            full_url = full_url.split('#')[0]
            parsed = urlparse(full_url)
            
            # Categorize by extension
            if any(full_url.endswith(ext) for ext in ['.js', '.jsx', '.ts', '.mjs']):
                results['js_files'].add(full_url)
            elif any(full_url.endswith(ext) for ext in ['.css', '.scss', '.sass', '.less']):
                results['css_files'].add(full_url)
            elif any(full_url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico']):
                results['images'].add(full_url)
            elif any(full_url.endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']):
                results['documents'].add(full_url)
            
            # Check if internal link
            if parsed.netloc == domain or not parsed.netloc:
                links.add(full_url)
            elif parsed.netloc:
                results['external_links'].add(full_url)
                if domain in parsed.netloc:
                    results['subdomains'].add(parsed.netloc)
        
        return links
    
    def extract_api_endpoints(text, base_url):
        """Extract API endpoints"""
        endpoints = set()
        patterns = [
            r'["\'](/api[^\s"\']+)["\']',
            r'["\'](/v\d+[^\s"\']+)["\']',
            r'["\'](/rest[^\s"\']+)["\']',
            r'["\'](/graphql)["\']',
            r'fetch\(["\']([^\s"\']+)["\']',
            r'axios\.(?:get|post|put|delete)\(["\']([^\s"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.I)
            for match in matches:
                if match.startswith('/'):
                    full_url = urljoin(base_url, match)
                    endpoints.add(full_url)
        
        return endpoints
    
    def detect_technologies(response):
        """Detect technologies"""
        techs = set()
        
        server = response.headers.get('Server', '')
        if server:
            techs.add(f"Server: {server}")
        
        powered = response.headers.get('X-Powered-By', '')
        if powered:
            techs.add(f"Powered by: {powered}")
        
        html = response.text.lower()
        
        tech_indicators = {
            'WordPress': ['wp-content', 'wp-includes', 'wp-json', 'wordpress'],
            'Elementor': ['elementor', 'elementor-widget'],
            'React': ['react', 'reactdom', '_reactroot'],
            'Vue.js': ['vue', 'v-', 'data-v-'],
            'Angular': ['ng-', 'angular', 'ngapp'],
            'jQuery': ['jquery', '$('],
            'Bootstrap': ['bootstrap', 'col-md-', 'container-fluid'],
            'Font Awesome': ['fontawesome', 'fa-'],
            'Google Analytics': ['google-analytics', 'gtag'],
            'Facebook Pixel': ['facebook.com/tr', 'fbq'],
        }
        
        for tech, indicators in tech_indicators.items():
            if any(indicator in html for indicator in indicators):
                techs.add(tech)
        
        return techs
    
    def crawl_url(url):
        """Crawl a single URL"""
        if url in visited or len(visited) >= max_pages:
            return []
        
        visited.add(url)
        
        try:
            start_time = time.time()
            response = session.get(url, timeout=10, verify=False, allow_redirects=True)
            response_time = time.time() - start_time
            
            results['response_times'].append(response_time)
            results['status_codes'][response.status_code] += 1
            
            if response.status_code == 200:
                print(f"{Colors.GREEN}✓{Colors.END} {url[:70]} ({response_time:.1f}s) | {Colors.CYAN}Emails: {len(results['emails'])}{Colors.END}")
                
                # Extract ALL emails
                emails = extract_all_emails(response.text, url)
                
                # Extract phone numbers
                phones = extract_phone_numbers(response.text)
                
                # Extract links and other data
                links = extract_links(response.text, url)
                api_endpoints = extract_api_endpoints(response.text, url)
                techs = detect_technologies(response)
                
                # Update results
                results['urls'].add(url)
                results['emails'].update(emails)
                results['phone_numbers'].update(phones)
                results['internal_links'].update(links)
                results['api_endpoints'].update(api_endpoints)
                results['technologies'].update(techs)
                
                # Extract parameters
                parsed = urlparse(url)
                if parsed.query:
                    params = parse_qs(parsed.query)
                    results['parameters'].update(params.keys())
                
                # Extract comments
                soup = BeautifulSoup(response.text, 'html.parser')
                comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text)
                for comment in comments:
                    if comment.strip() and len(comment.strip()) > 20:
                        results['comments'].append(comment.strip()[:300])
                
                # Extract forms
                for form in soup.find_all('form'):
                    form_info = {
                        'action': form.get('action', ''),
                        'method': form.get('method', 'GET'),
                        'inputs': len(form.find_all(['input', 'textarea', 'select']))
                    }
                    results['forms'].append(form_info)
                
                return list(links)
            
            elif response.status_code in [301, 302, 303, 307, 308]:
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    full_redirect = urljoin(url, redirect_url)
                    if full_redirect not in visited:
                        return [full_redirect]
            
            else:
                print(f"{Colors.WARNING}⚠{Colors.END} {url[:60]} -> {response.status_code}")
                
        except requests.Timeout:
            print(f"{Colors.FAIL}✗{Colors.END} {url[:60]} -> Timeout")
        except Exception as e:
            print(f"{Colors.FAIL}✗{Colors.END} {url[:60]} -> Error: {str(e)[:30]}")
        
        return []
    
    # Start crawling
    print(f"{Colors.CYAN}[*] Crawling {domain} - Extracting all emails and data{Colors.END}\n")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        while to_visit and len(visited) < max_pages:
            batch = list(to_visit)[:threads*2]
            to_visit -= set(batch)
            
            futures = {executor.submit(crawl_url, url): url for url in batch}
            
            for future in as_completed(futures):
                new_links = future.result()
                to_visit.update(set(new_links) - visited)
    
    elapsed = time.time() - start_time
    
    # Print results
    print(f"\n{Colors.CYAN}{'━'*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}  ✅ CRAWL COMPLETE ({elapsed:.1f}s){Colors.END}")
    print(f"{Colors.CYAN}{'━'*70}{Colors.END}\n")
    
    # EMAIL RESULTS - Most Important
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}  📧 EMAIL HARVESTING RESULTS{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}\n")
    
    if results['emails']:
        print(f"{Colors.BOLD}Total Emails Found: {Colors.GREEN}{len(results['emails'])}{Colors.END}\n")
        
        # Categorize emails
        professional = []
        personal = []
        role_based = []
        educational = []
        
        for email in sorted(results['emails']):
            if domain in email:
                professional.append(email)
            elif any(x in email for x in ['gmail', 'yahoo', 'hotmail', 'outlook', 'aol']):
                personal.append(email)
            elif any(x in email.split('@')[0] for x in ['info', 'admin', 'support', 'contact', 'webmaster', 'careers', 'hr', 'sales']):
                role_based.append(email)
            elif '.edu' in email:
                educational.append(email)
            else:
                professional.append(email)  # Default to professional
        
        # Display Professional Emails
        if professional:
            print(f"{Colors.BOLD}{Colors.CYAN}🏢 Professional Emails ({len(professional)}):{Colors.END}")
            for i, email in enumerate(professional, 1):
                print(f"  {i:2}. {Colors.GREEN}{email}{Colors.END}")
        
        # Display Role-Based Emails
        if role_based:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}📋 Role-Based Emails ({len(role_based)}):{Colors.END}")
            for i, email in enumerate(role_based, 1):
                print(f"  {i:2}. {email}")
        
        # Display Educational Emails
        if educational:
            print(f"\n{Colors.BOLD}{Colors.BLUE}🎓 Educational Emails ({len(educational)}):{Colors.END}")
            for i, email in enumerate(educational, 1):
                print(f"  {i:2}. {email}")
        
        # Display Personal Emails
        if personal:
            print(f"\n{Colors.BOLD}{Colors.WARNING}👤 Personal Emails ({len(personal)}):{Colors.END}")
            for i, email in enumerate(personal[:20], 1):
                print(f"  {i:2}. {email}")
        
        # Show email context samples
        if results['emails_with_context']:
            print(f"\n{Colors.BOLD}{Colors.CYAN}📝 Email Context Samples:{Colors.END}")
            for i, item in enumerate(results['emails_with_context'][:5], 1):
                print(f"\n  {i}. {Colors.GREEN}{item['email']}{Colors.END}")
                print(f"     Found on: {item['source'][:60]}")
                if item['context']:
                    print(f"     Context: {item['context'][:120]}...")
    
    else:
        print(f"{Colors.WARNING}⚠ No emails found!{Colors.END}")
    
    # Phone Numbers
    if results['phone_numbers']:
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}📞 PHONE NUMBERS FOUND ({len(results['phone_numbers'])}):{Colors.END}")
        for i, phone in enumerate(list(results['phone_numbers'])[:30], 1):
            print(f"  {i:2}. {phone}")
    
    # Statistics
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}📊 CRAWL STATISTICS{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}")
    print(f"  • Pages crawled: {len(visited)}/{max_pages}")
    print(f"  • Total emails: {Colors.GREEN}{len(results['emails'])}{Colors.END}")
    print(f"  • Phone numbers: {len(results['phone_numbers'])}")
    print(f"  • Internal links: {len(results['internal_links'])}")
    print(f"  • External links: {len(results['external_links'])}")
    print(f"  • Subdomains: {len(results['subdomains'])}")
    print(f"  • JS files: {len(results['js_files'])}")
    print(f"  • CSS files: {len(results['css_files'])}")
    print(f"  • Images: {len(results['images'])}")
    print(f"  • Documents: {len(results['documents'])}")
    print(f"  • API endpoints: {len(results['api_endpoints'])}")
    print(f"  • Parameters: {len(results['parameters'])}")
    print(f"  • Forms: {len(results['forms'])}")
    
    if results['response_times']:
        avg_time = sum(results['response_times']) / len(results['response_times'])
        print(f"  • Avg response time: {avg_time:.2f}s")
    
    # Technologies
    if results['technologies']:
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔧 DETECTED TECHNOLOGIES:{Colors.END}")
        for tech in sorted(results['technologies']):
            print(f"  • {tech}")
    
    # Subdomains
    if results['subdomains']:
        print(f"\n{Colors.BOLD}{Colors.CYAN}🌐 SUBDOMAINS FOUND:{Colors.END}")
        for sub in sorted(results['subdomains'])[:15]:
            print(f"  • {sub}")
    
    # API Endpoints
    if results['api_endpoints']:
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔌 API ENDPOINTS:{Colors.END}")
        for api in sorted(results['api_endpoints'])[:15]:
            print(f"  • {api}")
    
    # Save comprehensive report
    timestamp = int(time.time())
    domain_clean = domain.replace('.', '_')
    
    # Save all emails to file
    email_file = f"emails_{domain_clean}_{timestamp}.txt"
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write(f"Email Harvest Results - {target_url}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Emails: {len(results['emails'])}\n")
        f.write(f"{'='*70}\n\n")
        
        for email in sorted(results['emails']):
            f.write(f"{email}\n")
        
        if results['emails_with_context']:
            f.write(f"\n\n{'='*70}\n")
            f.write("EMAILS WITH CONTEXT:\n")
            f.write(f"{'='*70}\n\n")
            for item in results['emails_with_context']:
                f.write(f"Email: {item['email']}\n")
                f.write(f"Source: {item['source']}\n")
                f.write(f"Context: {item['context']}\n")
                f.write(f"{'-'*50}\n\n")
    
    # Save phone numbers
    phone_file = f"phones_{domain_clean}_{timestamp}.txt"
    with open(phone_file, 'w', encoding='utf-8') as f:
        f.write(f"Phone Numbers Found - {target_url}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(results['phone_numbers'])}\n")
        f.write(f"{'='*70}\n\n")
        for phone in sorted(results['phone_numbers']):
            f.write(f"{phone}\n")
    
    # Save full report
    full_report = f"xophy_report_{domain_clean}_{timestamp}.txt"
    with open(full_report, 'w', encoding='utf-8') as f:
        f.write(f"XOPHY ELITE - COMPLETE CRAWL REPORT\n")
        f.write(f"{'='*70}\n")
        f.write(f"Target: {target_url}\n")
        f.write(f"Domain: {domain}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {elapsed:.1f} seconds\n")
        f.write(f"Pages Crawled: {len(visited)}\n\n")
        
        f.write("EMAILS FOUND:\n")
        f.write(f"{'-'*40}\n")
        for email in sorted(results['emails']):
            f.write(f"{email}\n")
        
        f.write(f"\nPHONE NUMBERS:\n")
        f.write(f"{'-'*40}\n")
        for phone in sorted(results['phone_numbers']):
            f.write(f"{phone}\n")
        
        f.write(f"\nTECHNOLOGIES:\n")
        f.write(f"{'-'*40}\n")
        for tech in sorted(results['technologies']):
            f.write(f"{tech}\n")
        
        f.write(f"\nSUBDOMAINS:\n")
        f.write(f"{'-'*40}\n")
        for sub in sorted(results['subdomains']):
            f.write(f"{sub}\n")
        
        f.write(f"\nAPI ENDPOINTS:\n")
        f.write(f"{'-'*40}\n")
        for api in sorted(results['api_endpoints']):
            f.write(f"{api}\n")
    
    print(f"\n{Colors.GREEN}✓ Reports saved:{Colors.END}")
    print(f"  • Emails: {email_file}")
    print(f"  • Phone numbers: {phone_file}")
    print(f"  • Full report: {full_report}")
    print(f"\n{Colors.CYAN}{'━'*70}{Colors.END}\n")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        threads = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        run(target, max_pages, threads)
    else:
        print(f"{Colors.WARNING}Usage: python xophy_ultimate.py <target_url> [max_pages] [threads]{Colors.END}")
        print(f"{Colors.CYAN}Example: python xophy_ultimate.py https://case.edu.pk 200 30{Colors.END}")
