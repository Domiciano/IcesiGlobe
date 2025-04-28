#!/usr/bin/env python3
"""
dijkstra_flights.py
------------------------------------------------------------------------
Algoritmo de Dijkstra sobre el grafo de vuelos (JSON) construido
anteriormente.

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
# Carga del grafo
# ---------------------------------------------------------------------

JSON_PATH = "../data/full_flight_graph.json"        

def load_graph(path: str = JSON_PATH) -> Dict[str, Dict[str, Dict]]:
    if not Path(path).is_file():
        raise FileNotFoundError(f"No se encontró {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------------------
# Dijkstra genérico
# ---------------------------------------------------------------------

def dijkstra(
    graph: Dict[str, Dict[str, Dict]],
    origin: str,
    target: str,
    weight_key: str = "duration_hours",
) -> Tuple[float, List[str]]:
    """
    Devuelve (distancia_total, ruta) usando weight_key como costo.
    Si no existe ruta, lanza ValueError.
    """
    if origin not in graph:
        raise ValueError(f"País origen no está en el grafo: {origin}")
    if target not in graph:
        raise ValueError(f"País destino no está en el grafo: {target}")

    # Min-heap: (dist_acumulada, nodo_actual, ruta_hasta_ahora)
    pq: List[Tuple[float, str, List[str]]] = [(0.0, origin, [origin])]
    # Distancias definitivas
    best: Dict[str, float] = {origin: 0.0}

    while pq:
        dist, node, path = heapq.heappop(pq)
        if node == target:
            return dist, path

        # Si sacamos del heap un camino peor que el mejor conocido, lo saltamos
        if dist > best.get(node, float("inf")):
            continue

        for neighbour, attrs in graph[node].items():
            w = attrs.get(weight_key)
            if w is None:
                # Si ese enlace no tiene el atributo elegido, ignóralo
                continue
            new_dist = dist + w
            if new_dist < best.get(neighbour, float("inf")):
                best[neighbour] = new_dist
                heapq.heappush(pq, (new_dist, neighbour, path + [neighbour]))

    raise ValueError(f"No hay ruta entre {origin} y {target}")

# ---------------------------------------------------------------------
# Ejecución desde CLI
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Encuentra la ruta óptima (Dijkstra) entre dos países"
    )
    parser.add_argument("origin", help="País de origen, exactamente como en el JSON")
    parser.add_argument("target", help="País de destino")
    parser.add_argument(
        "--weight",
        default="duration_hours",
        choices=["duration_hours", "price_usd", "hops"],
        help="Atributo a minimizar (default: duration_hours)",
    )
    parser.add_argument(
        "--json",
        default=JSON_PATH,
        help="Ruta al archivo JSON (default: selected_flight_graph.json)",
    )
    args = parser.parse_args()

    graph = load_graph(args.json)

    try:
        total, path = dijkstra(graph, args.origin, args.target, args.weight)
        print(f"\nMejor ruta minimizando '{args.weight}':")
        print("  →  ".join(path))
        print(f"\nTotal {args.weight}: {total}\n")
    except ValueError as err:
        print(f"ERROR: {err}")

if __name__ == "__main__":
    main()
