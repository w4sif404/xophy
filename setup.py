from setuptools import setup, find_packages

setup(
    name="xophy",
    version="1.0.0",
    author="W4siF_4o4",
    description="XOPHY - OSINT & Recon Framework",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "colorama",
        "python-whois",
        "dnspython",
        "requests",
        "shodan",
        "pillow",
        "pyOpenSSL",
        "beautifulsoup4",
        "rich",
        "aiohttp",
        "selenium",
        "lxml",
        "tldextract",
        "phonenumbers",
        "psutil",
        "pycountry",
        "geopy",
        "maigret",
        "stem",
        "cloudscraper",
        "reportlab",
        "xlsxwriter",
        "python-dotenv",
        "httpx",
        "dnspython",
    ],
    entry_points={
        "console_scripts": [
            "xophy=core.cli:main"
        ]
    }
)
