#!/usr/bin/env python3
"""
Genera realistic_flight_graph.json a partir de OpenFlights
y la lista de países que te interesa.

* Usa solo rutas directas existentes (sin escalas).
* Calcula duración = distancia / 900 km/h.
* Calcula precio  = 50 USD + 0.10 USD/km .
* Añade 'hops': 0     (todos son vuelos directos).

Requisitos:
    pip install haversine pandas
"""

import json, csv, math, argparse
from collections import defaultdict
from haversine import haversine

# ---------------------------------------------------------------------
# 1. Carga de aeropuertos
# ---------------------------------------------------------------------

def load_airports(path="../graphData/airports.dat"):
    """
    Devuelve:  iata -> (country, (lat, lon), is_international)
    Marcamos is_international=True si type!='small_airport' y tiene IATA.
    """
    airports = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            (
                _id, name, city, country, iata, icao,
                lat, lon, alt, tz, dst, tz_db, ttype, src
            ) = row
            if not iata or len(iata) != 3:           # sin código IATA usable
                continue
            is_intl = ttype not in ("small_airport", "closed")
            airports[iata] = (
                country,
                (float(lat), float(lon)),
                is_intl
            )
    return airports

# ---------------------------------------------------------------------
# 2. Carga de rutas (solo directas, sin código compartido)
# ---------------------------------------------------------------------

def load_routes(path="../graphData/routes.dat"):
    """
    Yields (source_IATA, dest_IATA) para vuelos directos.
    Ignora rutas con IATA vacíos o códigos '\\N'.
    """
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            airline, airline_id, src, src_id, dst, dst_id, codeshare, stops, equip = row
            if len(src) == 3 and len(dst) == 3 and src != "\\N" and dst != "\\N":
                yield src, dst

# ---------------------------------------------------------------------
# 3. Construcción del grafo por país
# ---------------------------------------------------------------------

def build_graph(airports, routes, country_subset=None):
    graph = defaultdict(lambda: defaultdict(dict))

    for src, dst in routes:
        if src not in airports or dst not in airports:
            continue
        ctry_src, (lat_s, lon_s), intl_src = airports[src]
        ctry_dst, (lat_d, lon_d), intl_dst = airports[dst]

        # Filtra por países que realmente quieres
        if country_subset and (ctry_src not in country_subset or ctry_dst not in country_subset):
            continue

        distance_km = haversine((lat_s, lon_s), (lat_d, lon_d))
        duration = round(distance_km / 900, 2)                       # h
        price    = round(50 + 0.10 * distance_km, 2)                # USD

        graph[ctry_src][ctry_dst] = {
            "duration_hours": duration,
            "price_usd": price,
            "hops": 0
        }

    return graph

# ---------------------------------------------------------------------
# 4. CLI
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Construye realistic_flight_graph.json con rutas directas reales")
    parser.add_argument("--countries-txt", required=True,
                        help="Fichero TXT con la lista de países (uno por línea)")
    parser.add_argument("--airports", default="airports.dat")
    parser.add_argument("--routes",   default="routes.dat")
    parser.add_argument("--out",      default="realistic_flight_graph.json")
    args = parser.parse_args()

    # lee tu lista de países
    with open(args.countries_txt, encoding="utf-8") as f:
        wanted = {line.strip() for line in f if line.strip()}

    airports = load_airports(args.airports)
    routes   = load_routes(args.routes)

    graph = build_graph(airports, routes, wanted)

    # Guarda
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    print(f"Grafo guardado en {args.out} — países incluidos: {len(graph)}")

if __name__ == "__main__":
    main()
