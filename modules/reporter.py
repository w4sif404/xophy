# modules/reporter.py

import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


REPORT_DIR = "reports"


def ensure_dir():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)


def export_json(domain, data):
    ensure_dir()
    path = f"{REPORT_DIR}/{domain}.json"

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    return path


def export_pdf(domain, data):
    ensure_dir()
    path = f"{REPORT_DIR}/{domain}.pdf"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 40
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "XOPHY – Target Intelligence Report")

    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Target: {domain}")
    y -= 15
    c.drawString(40, y, f"Generated: {datetime.utcnow()} UTC")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Summary")
    y -= 15
    c.setFont("Helvetica", 10)

    for key, value in data.items():
        if isinstance(value, (list, dict)):
            continue
        c.drawString(50, y, f"{key}: {value}")
        y -= 12

        if y < 60:
            c.showPage()
            y = height - 40

    # Vulnerabilities
    vulns = data.get("vulnerabilities", [])
    if vulns:
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "Detected Vulnerabilities")
        y -= 15
        c.setFont("Helvetica", 10)

        for v in vulns:
            c.drawString(50, y, f"- {v}")
            y -= 12

            if y < 60:
                c.showPage()
                y = height - 40

    c.save()
    return path
