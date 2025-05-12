import json
import heapq

def calculate_distance(price_usd):
    return (price_usd - 50) / 0.10

def dijkstra(graph, source_id, destination_id):
    distances = {node: float('inf') for node in graph}
    distances[source_id] = 0
    previos = {}
    heap = [(0, source_id)]

    while heap:
        actual_distance, actual_node = heapq.heappop(heap)

        if actual_node == destination_id:
            break

        for neighboor_node, datos_conexion in graph[actual_node]["connections"].items():
            distance = calculate_distance(datos_conexion["price_usd"])
            new_distance = actual_distance + distance

            if new_distance < distances[neighboor_node]:
                distances[neighboor_node] = new_distance
                previos[neighboor_node] = actual_node
                heapq.heappush(heap, (new_distance, neighboor_node))

    
    if distances[destination_id] == float('inf'):
        return []  # cuando no hay path la lista esta vacia, de momento no encontre ningun caso que esto pase, pero estare pendiente

    path_reverso = []
    actual = destination_id
    while actual != source_id:
        path_reverso.append(actual)
        actual = previos.get(actual)
        if actual is None:
            return [] 
    path_reverso.append(source_id)
    path = list(reversed(path_reverso))


    resultado = []
    acumulado = 0
    for i in range(len(path)):
        if i == 0:
            resultado.append({"id": path[i], "distance": 0})
        else:
            prev = path[i - 1]
            curr = path[i]
            salto = calculate_distance(graph[prev]["connections"][curr]["price_usd"])
            acumulado += salto
            resultado.append({"id": curr, "distance": acumulado})

    return resultado


with open('c:/Users/mateo/Desktop/Semestre 8/Interactiva/IcesiGlobe/data/realistic_flight_graph.json', 'r') as f:
    grafo = json.load(f)

camino = dijkstra(grafo, "133", "32") 
for paso in camino:
    print(paso)