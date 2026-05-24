#!/bin/bash
echo "[*] Installing dependencies..."
sudo apt install -y python3-pip pkg-config python3-dev
pip install -r requirements.txt
echo "[+] Done! Run: python3 xophy.py"
