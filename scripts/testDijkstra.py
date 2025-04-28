#!/usr/bin/env python3
"""
dijkstra_flights.py
------------------------------------------------------------------------
Algoritmo de Dijkstra sobre el grafo de vuelos (JSON) construido
anteriormente, usando IDs internos pero mostrando nombres de país.

Uso rápido -------------------------------------------------------------
$ python dijkstra_flights.py  "Argentina"  "China"  --weight duration_hours
------------------------------------------------------------------------
"""

import json
import heapq
import argparse
from pathlib import Path
from typing import Dict, Tuple, List

# ---------------------------------------------------------------------
# Carga del grafo y de countries.json
# ---------------------------------------------------------------------

JSON_PATH = "../data/realistic_flight_graph.json"
COUNTRIES_JSON_PATH = "../data/countries.json"

def load_graph(path: str = JSON_PATH) -> Dict[str, Dict]:
    if not Path(path).is_file():
        raise FileNotFoundError(f"No se encontró {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_countries(path: str = COUNTRIES_JSON_PATH) -> Tuple[Dict[str, str], Dict[str, str]]:
    if not Path(path).is_file():
        raise FileNotFoundError(f"No se encontró {path}")
    with open(path, encoding="utf-8") as f:
        countries = json.load(f)
    name_to_id = {data['name']: cid for cid, data in countries.items()}
    id_to_name = {cid: data['name'] for cid, data in countries.items()}
    return name_to_id, id_to_name

# ---------------------------------------------------------------------
# Dijkstra genérico
# ---------------------------------------------------------------------

def dijkstra(
    graph: Dict[str, Dict],
    origin: str,
    target: str,
    weight_key: str = "duration_hours",
) -> Tuple[float, List[str]]:
    """
    Devuelve (distancia_total, ruta de IDs) usando weight_key como costo.
    Si no existe ruta, lanza ValueError.
    """
    if origin not in graph:
        raise ValueError(f"País origen (ID) no está en el grafo: {origin}")
    if target not in graph:
        raise ValueError(f"País destino (ID) no está en el grafo: {target}")

    pq: List[Tuple[float, str, List[str]]] = [(0.0, origin, [origin])]
    best: Dict[str, float] = {origin: 0.0}

    while pq:
        dist, node, path = heapq.heappop(pq)
        if node == target:
            return dist, path

        if dist > best.get(node, float("inf")):
            continue

        for neighbour, attrs in graph[node]["connections"].items():
            w = attrs.get(weight_key)
            if w is None:
                continue
            new_dist = dist + w
            if new_dist < best.get(neighbour, float("inf")):
                best[neighbour] = new_dist
                heapq.heappush(pq, (new_dist, neighbour, path + [neighbour]))

    raise ValueError(f"No hay ruta entre {origin} y {target}")

# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Encuentra la ruta óptima (Dijkstra) entre dos países (usando nombres)"
    )
    parser.add_argument("origin", help="País de origen (nombre)")
    parser.add_argument("target", help="País de destino (nombre)")
    parser.add_argument(
        "--weight",
        default="duration_hours",
        choices=["duration_hours", "price_usd", "hops"],
        help="Atributo a minimizar (default: duration_hours)",
    )
    parser.add_argument(
        "--json",
        default=JSON_PATH,
        help="Ruta al archivo JSON del grafo (default: realistic_flight_graph.json)",
    )
    parser.add_argument(
        "--countries-json",
        default=COUNTRIES_JSON_PATH,
        help="Ruta al archivo JSON de países (default: countries.json)",
    )
    args = parser.parse_args()

    graph = load_graph(args.json)
    name_to_id, id_to_name = load_countries(args.countries_json)

    # Verifica que los nombres existen
    if args.origin not in name_to_id:
        raise ValueError(f"Nombre de país origen no encontrado: {args.origin}")
    if args.target not in name_to_id:
        raise ValueError(f"Nombre de país destino no encontrado: {args.target}")

    origin_id = name_to_id[args.origin]
    target_id = name_to_id[args.target]

    try:
        total, path_ids = dijkstra(graph, origin_id, target_id, args.weight)
        path_names = [id_to_name[pid] for pid in path_ids]

        print(f"\nMejor ruta minimizando '{args.weight}':")
        print("  →  ".join(path_names))
        print(f"\nTotal {args.weight}: {total}\n")
    except ValueError as err:
        print(f"ERROR: {err}")

if __name__ == "__main__":
    main()
