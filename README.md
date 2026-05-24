```markdown
# XOPHY Framework

<p align="center">
  <img src="banner.PNG" alt="XOPHY Banner" width="100%">
</p>

<p align="center">
  <b>Multi-threaded intelligence gathering, infrastructure mapping, and target profiling engine.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-v3.0-000000?style=flat" alt="Version">
  <img src="https://img.shields.io/badge/Runtime-Python_3-000000?style=flat" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux_/_MacOS-000000?style=flat" alt="OS">
</p>

---

## Key Capabilities

XOPHY is built from the ground up to solve complex reconnaissance tasks efficiently. By running multi-threaded network scanners alongside automated web-mining scripts, it reduces a red-team's initial footprinting time from hours to minutes.

### Command Center Preview
<p align="center">
  <img src="main.PNG" alt="Xophy Main UI" width="90%">
</p>

---

## Architectural Breakdown

### 1. Infrastructure Reconnaissance
* **Tech-Stack & CVE Integration** — Audits web banners and extracts asset dependencies to map active software vulnerabilities.
* **DNS Profile Mapping** — Automatically interrogates host name nodes for deep `MX`, `TXT`, and `A` records.
* **SSL/TLS Diagnostics** — Deep-parses cryptographic handshake rules to evaluate overall security compliance.

### 2. Asset & Web Mining
* **DORK-o-Matic Pipeline** — Runs automated query blocks across search indexes to locate exposed configuration logs and indices.
* **Subdomain Enumeration** — Sweeps third-party records to identify hidden sub-assets and dangling CNAME redirects.
* **Social Footprint Recon** — Queries user profiles across 50+ unique platforms simultaneously using safe dynamic runtime fallbacks.

### 3. Intelligence Feeds
* **Ransom-Watch** — Monitors threat actor leak pages and updates an interactive active threat matrix.
* **IoT Discovery** — Leverages open asset indices to locate public-facing operational machinery and unauthenticated setups.
* **Watchtower Daemon** — Provides continuous real-time changes regarding target infrastructure health.

---

## Quick Start

Get your local framework up and running in a few simple steps:

```bash
git clone [https://github.com/w4sif404/xophy](https://github.com/w4sif404/xophy)
cd xophy
chmod +x install.sh && ./install.sh
python3 -m venv venv && source venv/bin/activate
python3 core/cli.py
