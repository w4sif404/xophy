#!/usr/bin/env python3
"""
XOPHY Advanced DORK-o-Matic
Next-level Google Dorking Engine
Author: W4siF_4o4
"""

import webbrowser
import urllib.parse
from typing import List

# =========================
# XOPHY STANDARD INTERFACE
# =========================

def run():
    """
    Required entry point for XOPHY module loader
    """
    xophy_entry()

# =========================
# INPUT HELPERS
# =========================

def ask_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("[!] Input cannot be empty. Try again.")

def ask_open_mode() -> bool:
    print("\nChoose Dork Output Mode:")
    print("[1] Show dorks in terminal")
    print("[2] Open dorks in browser")
    choice = input("Select option > ").strip()
    return choice == "2"

# =========================
# GOOGLE SEARCH URL
# =========================

def google_url(query: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

# =========================
# ADVANCED CREDENTIAL & SECRET DORKS
# =========================

CREDENTIAL_DORKS = {
    "ENV & CONFIG LEAKS": [
        'site:{t} ext:env',
        'site:{t} ext:config',
        'site:{t} ext:yaml',
        'site:{t} ext:yml',
        'site:{t} ext:json "password"',
        'site:{t} ext:ini',
        'site:{t} ext:properties',
    ],

    "DATABASE & CONNECTION STRINGS": [
        '"{t}" "DB_PASSWORD"',
        '"{t}" "DATABASE_URL"',
        '"{t}" "connection_string"',
        '"{t}" "mongodb://"',
        '"{t}" "postgres://"',
        '"{t}" "mysql://"',
    ],

    "CLOUD KEYS (HIGH IMPACT)": [
        '"{t}" "AWS_ACCESS_KEY_ID"',
        '"{t}" "AWS_SECRET_ACCESS_KEY"',
        '"{t}" "aws_access_key"',
        '"{t}" "aws_secret"',
        '"{t}" "AZURE_STORAGE_KEY"',
        '"{t}" "GOOGLE_API_KEY"',
    ],

    "TOKEN & AUTH LEAKS": [
        '"{t}" "Bearer "',
        '"{t}" "Authorization:"',
        '"{t}" "access_token"',
        '"{t}" "refresh_token"',
        '"{t}" "id_token"',
    ],

    "PRIVATE KEYS & CERTIFICATES": [
        '"{t}" "-----BEGIN PRIVATE KEY-----"',
        '"{t}" "-----BEGIN RSA PRIVATE KEY-----"',
        '"{t}" "-----BEGIN OPENSSH PRIVATE KEY-----"',
        '"{t}" ext:pem',
        '"{t}" ext:key',
        '"{t}" ext:p12',
    ],

    "CI/CD & DEVOPS SECRETS": [
        '"{t}" "GITHUB_TOKEN"',
        '"{t}" "GITLAB_TOKEN"',
        '"{t}" "CI_JOB_TOKEN"',
        '"{t}" "JENKINS_URL"',
        '"{t}" "SLACK_TOKEN"',
    ],

    "LEAK PLATFORMS": [
        'site:pastebin.com "{t}"',
        'site:hastebin.com "{t}"',
        'site:ghostbin.com "{t}"',
        'site:rentry.co "{t}"',
        'site:controlc.com "{t}"',
    ],

    "SOURCE CODE PLATFORMS": [
        'site:github.com "{t}" password',
        'site:github.com "{t}" secret',
        'site:github.com "{t}" ".env"',
        'site:gitlab.com "{t}" password',
        'site:bitbucket.org "{t}" secret',
    ],
}

# =========================
# CORE ENGINE
# =========================

def run_credentials_dorking(target: str, open_browser: bool):
    print(f"\n▶ Running Credentials & Secrets on {target}\n")

    for category, dorks in CREDENTIAL_DORKS.items():
        print(f"=== {category} ===")
        for dork in dorks:
            query = dork.format(t=target)
            url = google_url(query)

            print(f"  ├─ {query}")
            print(f"  │  {url}")

            if open_browser:
                webbrowser.open(url)

        print("-" * 55)

# =========================
# XOPHY ENTRY POINT
# =========================

def xophy_entry():
    print("\n" + "=" * 60)
    print("  XOPHY ADVANCED DORK-O-MATIC :: CREDENTIALS & SECRETS")
    print("=" * 60)

    target = ask_non_empty("Enter DOMAIN / COMPANY / ORG name > ")
    open_browser = ask_open_mode()

    run_credentials_dorking(target, open_browser)

# =========================
# STANDALONE SUPPORT
# =========================

if __name__ == "__main__":
    xophy_entry()
