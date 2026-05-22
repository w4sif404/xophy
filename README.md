# XOPHY 🔍

![Xophy Banner](banner.PNG)

## Advanced OSINT & Infrastructure Intelligence Tool
XOPHY is a next-generation reconnaissance framework designed for **ethical OSINT, infrastructure analysis, and security research**.

### Interface Preview
![Xophy Main UI](main.PNG)

---

## 🚀 Features

### [01] Infrastructure Recon
* **Tech-Stack & CVE:** Identify server technologies and vulnerabilities.
* **DNS Enumeration:** Full MX, TXT, and A record mapping.
* **SSL/TLS Advanced:** Deep analysis of certificate security.

### [02] Web & Data Mining
* **DORK-o-Matic:** Automated Google Dorking for sensitive data.
* **Subdomain Enum:** Find hidden entry points and sub-assets.
* **Social Recon:** Deep search across social media footprints.

### [03] Network & Threats
* **Ransom-Watch (LIVE):** Track active ransomware threats and leaks.
* **IoT Discovery:** Locate connected devices and industrial assets.
* **Watchtower (Live):** Real-time monitoring of target infrastructure.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/w4sif404/xophy.git
# Enter the directory
cd xophy

# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the environment
# On Linux/Kali:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
# 4. Run The Tool
python3 core/cli.py
