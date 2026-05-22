from setuptools import setup, find_packages

setup(
    name="xophy",
    version="1.0.0",
    author="W4siF_4o4",
    description="XOPHY - OSINT & Recon Framework",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "colorama",
        "python-whois",
        "dnspython",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "xophy=core.cli:main"
        ]
    }
)
