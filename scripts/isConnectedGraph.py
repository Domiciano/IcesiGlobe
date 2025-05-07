#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida si el grafo de rutas aéreas es conexo.
Uso:
    python check_connectivity.py [ruta_al_json]
Si no se indica ruta toma 'realistic_flight_graph.json'
"""
import itertools
import json
import argparse
from collections import deque
from pathlib import Path


def load_graph(file_path: str) -> dict:
    """Lee el JSON y devuelve el diccionario Python."""
    with open(file_path, encoding="utf-8") as fh:
        return json.load(fh)


def build_undirected_adj(graph: dict) -> dict[str, set[str]]:
    """
    Genera un diccionario {nodo: {vecinos}} tratándolo como grafo no dirigido.
    """
    adj: dict[str, set[str]] = {}
    for src, dests in graph.items():
        adj.setdefault(src, set())
        for dst in dests:                          # cada clave dst es vecino de src
            adj[src].add(dst)
            adj.setdefault(dst, set()).add(src)   # añade conexión inversa
    return adj


def connected_components(adj: dict[str, set[str]]) -> list[set[str]]:
    """Devuelve la lista de componentes conexos usando BFS."""
    vistos: set[str] = set()
    comps: list[set[str]] = []

    for nodo in adj:
        if nodo in vistos:
            continue
        comp = set()
        cola: deque[str] = deque([nodo])
        while cola:
            v = cola.popleft()
            if v in vistos:
                continue
            vistos.add(v)
            comp.add(v)
            cola.extend(adj[v] - vistos)
        comps.append(comp)
    return comps


def main(file_path: str) -> None:
    graph = load_graph(file_path)
    adj   = build_undirected_adj(graph)
    comps = connected_components(adj)
    all_nodes = set(graph.keys()) | set(itertools.chain.from_iterable(graph.values()))
    num_vertices = len(all_nodes)
    print(f"Número total de vértices: {num_vertices}")
    if len(comps) == 1:
        print("✅ El grafo es conexo (todos los países están interconectados).")
    else:
        # Tomamos como “principal” el componente con más nodos
        principal = max(comps, key=len)
        aislados  = sorted({n for c in comps if c is not principal for n in c})
        print("⚠️  El grafo NO es conexo.")
        print(f"Componentes encontrados: {len(comps)}")
        print("Nodos sin acceso al componente principal:")
        for nodo in aislados:
            print(f"  · {nodo}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Comprueba la conectividad del grafo de vuelos.")
    parser.add_argument(
        "json_file", nargs="?", default="realistic_flight_graph.json",
        help="Ruta al archivo JSON (por defecto 'realistic_flight_graph.json').")
    args = parser.parse_args()
    main(args.json_file)





