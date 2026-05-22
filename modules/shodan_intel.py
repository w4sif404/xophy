
# modules/shodan_intel.py

import os
import shodan
from collections import defaultdict

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

def fetch_shodan_data(ip):
    if not SHODAN_API_KEY:
        return {"error": "Shodan API key not set"}

    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        host = api.host(ip)
    except Exception as e:
        return {"error": str(e)}

    vulns = host.get("vulns", [])
    services = []

    for item in host.get("data", []):
        services.append({
            "port": item.get("port"),
            "service": item.get("product"),
            "version": item.get("version")
        })

    return {
        "ip": ip,
        "org": host.get("org"),
        "os": host.get("os"),
        "ports": host.get("ports", []),
        "services": services,
        "vulns": vulns
    }
