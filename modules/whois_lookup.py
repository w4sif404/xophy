import whois
import datetime
import re

# -----------------------------
# Helpers
# -----------------------------

def clean(value, fallback="Not disclosed"):
    if value in [None, "", [], {}]:
        return fallback
    if isinstance(value, list):
        return list(set(value))
    return value

def parse_date(date):
    if isinstance(date, list):
        date = date[0]
    return date

def calculate_domain_age(creation_date):
    try:
        creation_date = parse_date(creation_date)
        age_days = (datetime.datetime.now() - creation_date).days
        return age_days
    except Exception:
        return None

def is_privacy_protected(data):
    privacy_keywords = [
        "privacy", "redacted", "whoisguard", "protected",
        "gdpr", "proxy", "masked"
    ]
    text = str(data).lower()
    return any(k in text for k in privacy_keywords)

def registrar_risk(registrar):
    risky = ["namecheap", "dynadot", "porkbun", "godaddy"]
    if not registrar:
        return "UNKNOWN"
    return "MEDIUM" if registrar.lower() in risky else "LOW"

# -----------------------------
# Main Engine
# -----------------------------

def run(domain):
    try:
        w = whois.whois(domain)

        creation = parse_date(w.creation_date)
        expiration = parse_date(w.expiration_date)
        age_days = calculate_domain_age(creation)

        privacy = is_privacy_protected(w)

        risk_score = 0
        risk_factors = []

        # Domain age risk
        if age_days is not None:
            if age_days < 30:
                risk_score += 40
                risk_factors.append("Very new domain (<30 days)")
            elif age_days < 180:
                risk_score += 20
                risk_factors.append("Recently registered domain")

        # Privacy protection
        if privacy:
            risk_score += 15
            risk_factors.append("WHOIS privacy masking detected")

        # Registrar risk
        registrar_level = registrar_risk(w.registrar)
        if registrar_level == "MEDIUM":
            risk_score += 10
            risk_factors.append("Common registrar used in abuse cases")

        # PK domain restriction
        pk_note = None
        if domain.endswith(".pk"):
            pk_note = "PK registry restricts public WHOIS visibility"

        # Final severity
        if risk_score >= 50:
            severity = "HIGH"
        elif risk_score >= 25:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return {
            "Domain": domain,
            "Status": "Registered",
            "Registrar": clean(w.registrar),
            "WHOIS Server": clean(w.whois_server),
            "Creation Date": str(creation),
            "Expiration Date": str(expiration),
            "Updated Date": str(parse_date(w.updated_date)),
            "Domain Age (days)": age_days,
            "Name Servers": clean(w.name_servers, []),
            "Registrant Organization": clean(w.org),
            "Registrant Country": clean(w.country),
            "Registrant Email": clean(w.emails),
            "DNSSEC": clean(w.dnssec),
            "Privacy Protected": privacy,
            "Registrar Risk": registrar_level,
            "Risk Score": risk_score,
            "Risk Severity": severity,
            "Risk Factors": risk_factors,
            "Note": pk_note
        }

    except Exception as e:
        return {
            "Domain": domain,
            "Status": "FAILED",
            "Error": str(e)
        }
