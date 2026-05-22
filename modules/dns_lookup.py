import dns.resolver
import dns.reversename
from concurrent.futures import ThreadPoolExecutor
from utils.colors import RED, YELLOW, RESET

def get_records(resolver, domain, rtype):
    """Internal helper to fetch specific record types."""
    try:
        answers = resolver.resolve(domain, rtype)
        if rtype == "MX":
            return [str(rdata.exchange).rstrip('.') for rdata in answers]
        elif rtype == "TXT":
            return ["".join([t.decode(errors="ignore") for t in rdata.strings]) for rdata in answers]
        elif rtype == "SOA":
            rdata = answers[0]
            return [f"Primary: {rdata.mname}, Admin: {rdata.rname}, Serial: {rdata.serial}"]
        else:
            return [str(rdata).rstrip('.') for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return []
    except Exception:
        return []

def check_wildcard(resolver, domain):
    """Detects if the domain has a wildcard DNS configuration."""
    wildcard_domain = f"xophy_test_random.{domain}"
    try:
        resolver.resolve(wildcard_domain, "A")
        return True
    except:
        return False

def reverse_dns(resolver, ip):
    """Performs reverse DNS lookup on found IP addresses."""
    try:
        addr = dns.reversename.from_address(ip)
        return str(resolver.resolve(addr, "PTR")[0]).rstrip('.')
    except:
        return None

def run(domain):
    """
    Advanced DNS Enumeration Module.
    Features: Multithreading, Wildcard Detection, SOA Analysis, and PTR Lookups.
    """
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1.5
    resolver.lifetime = 1.5
    
    # Advanced features dict
    results = {
        "Wildcard Detected": "No",
        "A": [],
        "AAAA": [],
        "MX": [],
        "NS": [],
        "TXT": [],
        "SOA": [],
        "PTR (Reverse)": []
    }

    # 1. Check for Wildcard DNS
    if check_wildcard(resolver, domain):
        results["Wildcard Detected"] = f"{RED}Yes (Expect False Positives){RESET}"

    # 2. Parallel Record Retrieval
    target_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA"]
    with ThreadPoolExecutor(max_workers=len(target_types)) as executor:
        future_to_type = {executor.submit(get_records, resolver, domain, rt): rt for rt in target_types}
        
        for future in future_to_type:
            rtype = future_to_type[future]
            results[rtype] = future.result()

    # 3. Intelligent PTR (Reverse DNS) for A records
    if results["A"]:
        unique_ips = list(set(results["A"]))
        for ip in unique_ips[:5]: # Limit to first 5 to keep it fast
            ptr = reverse_dns(resolver, ip)
            if ptr:
                results["PTR (Reverse)"].append(f"{ip} -> {ptr}")

    # Clean up empty lists for a cleaner UI
    return {k: (v if v else "Not Found") for k, v in results.items()}
