# 🔍 XOPHY Framework v3.0

<p align="center">
  <img src="banner.PNG" alt="XOPHY Banner" width="100%">
</p>

<p align="center">
  <strong>Next-Generation Open-Source Intelligence (OSINT) & Infrastructure Reconnaissance Engine</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0_Stable-00ff66?style=flat-square&logo=github&logoColor=white" alt="Version">
  <img src="https://img.shields.io/badge/Language-Python_3.x-007acc?style=flat-square&logo=python&logoColor=white" alt="Language">
  <img src="https://img.shields.io/badge/Environment-Linux_/_Kali-black?style=flat-square&logo=kali-linux&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-red?style=flat-square" alt="License">
</p>

---

## ⚡ Overview

XOPHY is an advanced, multi-threaded intelligence gathering and tactical reconnaissance framework built from scratch. Engineered for red teamers, penetration testers, and security researchers, it automates deep-dive information gathering across target networks, code repositories, web applications, and social footprints while implementing robust evasion and stealth controls.

### 🖥️ Interface Preview
<p align="center">
  <img src="main.PNG" alt="Xophy Main UI" width="90%" style="border: 2px solid #00ff66; border-radius: 5px;">
</p>

---

## 🚀 Core Modules & Capabilities

| Module Category | Feature Sub-Systems | Technical Capabilities |
| :--- | :--- | :--- |
| **01 🌐 Infrastructure Recon** | Tech-Stack & CVE <br> DNS Enumeration <br> SSL/TLS Advanced | • Identifies server-side technologies & queries historical CVE maps.<br>• Full MX, TXT, and A record structural mapping.<br>• Deep-dive cryptographic certificate strength evaluation. |
| **02 🕵️ Web & Data Mining** | DORK-o-Matic <br> Subdomain Enum <br> Social Recon | • Automated Google Dorking pipelines targeting leaked data leaks.<br>• Map hidden entry points, dangling CNAMEs, and sub-assets.<br>• High-fidelity multi-threaded target profile mapping across 50+ sites. |
| **03 📡 Network & Threats** | Ransom-Watch `LIVE`<br> IoT Discovery <br> Watchtower `LIVE` | • Monitors dark web ransomware groups & target disclosures in real-time.<br>• Pinpoints public-facing connected devices & industrial assets.<br>• High-frequency active monitoring of critical assets. |

---

## 🛠️ Installation & Setup

Set up the execution environment on your local system:

```bash
# Clone the tactical repository from source
git clone [https://github.com/w4sif404/xophy](https://github.com/w4sif404/xophy)
cd xophy

# Configure execution permissions and run dependencies deployment
chmod +x install.sh
./install.sh

# Isolate environment dependencies safely
python3 -m venv venv
source venv/bin/activate

# Initialize the interactive command center console
python3 core/cli.py
