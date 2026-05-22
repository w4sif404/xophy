#!/usr/bin/env python3

import os
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================
# CONFIG
# =========================

# Project root directory (…/xophy)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to wordlist
WORDLIST = os.path.join(BASE_DIR, "wordlists", "subdomains.txt")

THREADS = 50
TIMEOUT = 2.0


# =========================
# DNS Resolver
# =========================
def resolve_subdomain(subdomain):
    try:
        dns.resolver.resolve(subdomain, "A", lifetime=TIMEOUT)
        return subdomain
    except Exception:
        return None


# =========================
# Output Formatter
# =========================
def print_subdomains(subdomains):
    print("=" * 40)
    print("[ Subdomain Enumeration ]")
    print("=" * 40)
    print(f"Total Subdomains Found : {len(subdomains)}\n")

    for sub in subdomains:
        print(f"[+] {sub}")


# =========================
# Main Runner (XOPHY Mode)
# =========================
def run(domain, silent=False):
    """
    silent = False -> print results (Menu option 5)
    silent = True  -> return data only (Run All / profiler)
    """

    # Check wordlist existence
    if not os.path.exists(WORDLIST):
        if not silent:
            print(f"[-] Wordlist not found: {WORDLIST}")
        return []

    # Load subdomains from wordlist
    with open(WORDLIST, "r", encoding="utf-8", errors="ignore") as f:
        candidates = [
            f"{line.strip()}.{domain}"
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    found = []

    # Multi-threaded DNS resolution
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(resolve_subdomain, sub) for sub in candidates]

        for future in as_completed(futures):
            result = future.result()
            if result:
                found.append(result)

    # Deduplicate & sort
    found = sorted(set(found))

    # Print output if not silent
    if not silent:
        print_subdomains(found)

    return found

