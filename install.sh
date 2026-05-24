#!/bin/bash

echo "[*] Checking Python..."
python3 --version || { echo "[x] Python3 not found"; exit 1; }

echo "[*] Creating virtual environment..."
python3 -m venv venv

echo "[*] Activating venv..."
source venv/bin/activate

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing all dependencies..."
pip install requests
pip install beautifulsoup4
pip install python-whois
pip install dnspython
pip install reportlab
pip install aiohttp
pip install aiodns
pip install cryptography
pip install pillow
pip install shodan
pip install urllib3

echo ""
echo "================================================"
echo "[+] Installation complete!"
echo ""
echo "[*] EVERY TIME you run xophy, do this:"
echo ""
echo "    source venv/bin/activate"
echo "    python3 core/cli.py"
echo "================================================"
