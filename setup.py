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
        "requests",
        "beautifulsoup4",
        "python-whois",
        "dnspython",
        "reportlab",
        "aiohttp",
        "aiodns",
        "cryptography",
        "pillow",
        "shodan",
        "urllib3",
    ],
)
