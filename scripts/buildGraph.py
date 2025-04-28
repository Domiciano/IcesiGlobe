import json, csv, math, argparse
from collections import defaultdict
from haversine import haversine

# ---------------------------------------------------------------------
# 1. Carga de aeropuertos
# ---------------------------------------------------------------------

def load_airports(path="../graphData/airports.dat"):
    airports = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            (
                _id, name, city, country, iata, icao,
                lat, lon, alt, tz, dst, tz_db, ttype, src
            ) = row
            if not iata or len(iata) != 3:
                continue
            is_intl = ttype not in ("small_airport", "closed")
            airports[iata] = (
                country,
                (float(lat), float(lon)),
                is_intl
            )
    return airports

# ---------------------------------------------------------------------
# 2. Carga de rutas
# ---------------------------------------------------------------------

def load_routes(path="../graphData/routes.dat"):
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            airline, airline_id, src, src_id, dst, dst_id, codeshare, stops, equip = row
            if len(src) == 3 and len(dst) == 3 and src != "\\N" and dst != "\\N":
                yield src, dst

# ---------------------------------------------------------------------
# 3. Construcción del grafo por país
# ---------------------------------------------------------------------

def build_graph(airports, routes, country_subset, name_to_id):
    graph = defaultdict(lambda: {"country_name": "", "connections": {}})

    for src, dst in routes:
        if src not in airports or dst not in airports:
            continue
        ctry_src, (lat_s, lon_s), intl_src = airports[src]
        ctry_dst, (lat_d, lon_d), intl_dst = airports[dst]

        # Filtra por países que realmente quieres
        if ctry_src not in country_subset or ctry_dst not in country_subset:
            continue

        # Verificar que ambos países existen en name_to_id
        if ctry_src not in name_to_id:
            raise ValueError(f"Error: país de origen '{ctry_src}' no encontrado en countries.json")
        if ctry_dst not in name_to_id:
            raise ValueError(f"Error: país destino '{ctry_dst}' no encontrado en countries.json")

        src_id = name_to_id[ctry_src]
        dst_id = name_to_id[ctry_dst]

        distance_km = haversine((lat_s, lon_s), (lat_d, lon_d))
        duration = round(distance_km / 900, 2)
        price    = round(50 + 0.10 * distance_km, 2)

        # Añade el nombre de país si no estaba
        graph[src_id]["country_name"] = ctry_src

        # Agrega la conexión
        graph[src_id]["connections"][dst_id] = {
            "country_name": ctry_dst,
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
        description="Construye realistic_flight_graph.json con rutas directas reales usando IDs de países")
    parser.add_argument("--countries-txt", required=True,
                        help="Fichero TXT con la lista de países (uno por línea)")
    parser.add_argument("--countries-json", required=True,
                        help="Archivo JSON con la información de países y sus IDs (countries.json)")
    parser.add_argument("--airports", default="airports.dat")
    parser.add_argument("--routes",   default="routes.dat")
    parser.add_argument("--out",      default="realistic_flight_graph.json")
    args = parser.parse_args()

    # Cargar países permitidos
    with open(args.countries_txt, encoding="utf-8") as f:
        wanted = {line.strip() for line in f if line.strip()}

    # Cargar countries.json y mapear name -> id
    with open(args.countries_json, encoding="utf-8") as f:
        countries = json.load(f)
    name_to_id = {data['name']: cid for cid, data in countries.items()}

    airports = load_airports(args.airports)
    routes   = load_routes(args.routes)

    graph = build_graph(airports, routes, wanted, name_to_id)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

    print(f"Grafo guardado en {args.out} — países incluidos: {len(graph)}")

if __name__ == "__main__":
    main()
