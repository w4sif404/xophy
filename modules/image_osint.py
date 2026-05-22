#!/usr/bin/env python3

from bs4 import BeautifulSoup

import requests

import os



AVATAR_DIR = "reports/avatars"



def scrape_avatar(url, platform, username):

    """

    Downloads a profile picture from a platform and saves it.

    """

    if not os.path.exists(AVATAR_DIR):

        os.makedirs(AVATAR_DIR)



    try:

        # Most platforms hide the real image URL in meta tags

        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(r.text, "html.parser")

        

        # Look for OpenGraph image tags (Standard for social media)

        img_tag = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})

        

        if img_tag and img_tag.get("content"):

            img_url = img_tag["content"]

            img_data = requests.get(img_url).content

            

            filename = f"{AVATAR_DIR}/{username}_{platform}.jpg"

            with open(filename, "wb") as f:

                f.write(img_data)

            return filename

    except Exception:

        return None

    return None

import os

import subprocess

import requests

from PIL import Image

from utils.colors import GREEN, CYAN, YELLOW, RED, RESET



IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

REPORT_DIR = "reports/geotags"



# =========================

# UI

# =========================

def banner(title):

    print(CYAN + "\n" + "=" * 60)

    print(f"[ {title} ]")

    print("=" * 60 + RESET)



def is_image(filename):

    return filename.lower().endswith(IMAGE_EXTENSIONS)



# =========================

# GPS PARSER

# =========================

def dms_to_decimal(dms):

    dms = dms.replace("deg", "").replace('"', "").replace("'", "")

    parts = dms.split()

    deg, minute, sec = map(float, parts[:3])

    return deg + minute / 60 + sec / 3600



def extract_gps(exif):

    lat = lon = None



    for line in exif.splitlines():

        if "GPS Latitude" in line and "Ref" not in line:

            lat = line.split(":", 1)[1].strip()

        if "GPS Longitude" in line and "Ref" not in line:

            lon = line.split(":", 1)[1].strip()



    if not lat or not lon:

        return None, None



    return dms_to_decimal(lat), dms_to_decimal(lon)



# =========================

# SATELLITE IMAGE

# =========================

def download_satellite(lat, lon, name):

    api_key = os.getenv("LOCATIONIQ_API_KEY")

    if not api_key:

        print(RED + "    [ERROR] LOCATIONIQ_API_KEY not set" + RESET)

        return



    os.makedirs(REPORT_DIR, exist_ok=True)



    url = (

        "https://maps.locationiq.com/v3/staticmap"

        f"?key={api_key}&center={lat},{lon}"

        "&zoom=18&size=600x600&maptype=satellite"

    )



    out = f"{REPORT_DIR}/{name}_satellite.png"

    r = requests.get(url, timeout=15)



    if r.status_code == 200:

        with open(out, "wb") as f:

            f.write(r.content)

        print(GREEN + f"    🛰️ Satellite saved → {out}" + RESET)

    else:

        print(RED + "    [ERROR] Satellite fetch failed" + RESET)



# =========================

# MAIN ENTRY (CLI IMPORT)

# =========================

def run(directory):

    banner("Image OSINT :: Metadata + Geolocation")



    if not os.path.isdir(directory):

        print(RED + "[ERROR] Directory not found." + RESET)

        return



    images = [f for f in os.listdir(directory) if is_image(f)]



    if not images:

        print(YELLOW + "[!] No images found." + RESET)

        return



    for image in images:

        path = os.path.join(directory, image)

        name = os.path.splitext(image)[0]



        print(CYAN + f"\n[+] Processing: {image}" + RESET)



        try:

            img = Image.open(path)

            print(GREEN + f"    Size: {img.size}" + RESET)

        except Exception:

            print(RED + "    [ERROR] Cannot open image" + RESET)

            continue



        result = subprocess.run(

            ["exiftool", "-a", "-g1", path],

            stdout=subprocess.PIPE,

            stderr=subprocess.DEVNULL,

            text=True

        )



        exif = result.stdout.strip()

        print(exif)



        lat, lon = extract_gps(exif)



        if lat and lon:

            print(GREEN + f"\n    📍 GPS: {lat}, {lon}" + RESET)

            print(GREEN + f"    🌍 Maps: https://www.google.com/maps/@{lat},{lon},18z" + RESET)

            download_satellite(lat, lon, name)

        else:

            print(YELLOW + "\n    📍 GPS: Not available" + RESET)



        print(CYAN + "-" * 60 + RESET)



    print(GREEN + "\n[✓] Image OSINT Completed\n" + RESET)
