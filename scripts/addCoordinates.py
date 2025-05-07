#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geocode_countries.py

Reads a JSON of countries with English names, queries Nominatim
to obtain latitude and longitude for each, and produces:
  - coords.json
  - countries_with_coords.json

Usage:
  python geocode_countries.py --input countries.json
"""

import json
import time
import argparse
import requests

# Adjust this USER_AGENT to identify your application/project
USER_AGENT = "curaca492@gmail.com - geocode_countries_script/1.0"

def load_countries(path: str) -> dict:
    """
    Load the countries JSON file and return its contents as a dict.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def geocode(name: str) -> tuple[float|None, float|None]:
    """
    Query Nominatim for the given country name and return (lat, lon) as floats.
    Returns (None, None) if no results are found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": name,
        "format": "jsonv2",
        "limit": 1
    }
    headers = {
        "User-Agent": USER_AGENT
    }
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None, None
    # Nominatim returns lat/lon as strings
    return float(data[0]["lat"]), float(data[0]["lon"])

def main():
    # Load the input countries JSON
    input_path = "../data/countries.json"
    countries = load_countries(input_path)
    coords: dict[str, dict[str, float|None]] = {}
    enriched: dict[str, dict] = {}

    for country_id, info in countries.items():
        name = info.get("name")
        if not name:
            continue

        print(f"Geocoding «{name}»…", end=" ")
        lat, lon = geocode(name)
        if lat is None:
            print("❌ not found")
        else:
            print(f"✅ ({lat:.4f}, {lon:.4f})")

        # Save into coords mapping
        coords[name] = {"lat": lat, "lon": lon}

        # Enrich the original object
        enriched_obj = info.copy()
        enriched_obj["lat"] = lat
        enriched_obj["lon"] = lon
        enriched[country_id] = enriched_obj

        # Mandatory pause for Nominatim: 1 second between requests
        time.sleep(1)

    # Write coords.json
    with open("coords.json", "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=2)
    print("→ coords.json created")

    # Write countries_with_coords.json
    with open("countries_with_coords.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print("→ countries_with_coords.json created")


if __name__ == "__main__":
    main()

