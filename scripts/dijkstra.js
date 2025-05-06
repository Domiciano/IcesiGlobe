const fs = require('fs');
const path = require('path');

function calculateDistance(priceUsd) {
    return (priceUsd - 50) / 0.10;
}

function dijkstra(graph, sourceId, destinationId) {
    const distances = {};
    const previos = {};
    const heap = [];

    for (const node in graph) {
        distances[node] = Infinity;
    }

    distances[sourceId] = 0;
    heap.push({ id: sourceId, distance: 0 });

    while (heap.length > 0) {
        // js no tiene preority queue, así que toco hacer un sort
        heap.sort((a, b) => a.distance - b.distance);
        const { id: actualNode, distance: actualDistance } = heap.shift();

        if (actualNode === destinationId) break;

        const connections = graph[actualNode].connections;
        for (const neighborNode in connections) {
            const conn = connections[neighborNode];
            const distance = calculateDistance(conn.price_usd);
            const newDistance = actualDistance + distance;

            if (newDistance < distances[neighborNode]) {
                distances[neighborNode] = newDistance;
                previos[neighborNode] = actualNode;
                heap.push({ id: neighborNode, distance: newDistance });
            }
        }
    }

    if (distances[destinationId] === Infinity) return []; // cuando no hay path la lista esta vacia, de momento no encontre ningun caso que esto pase, pero estare pendiente

    
    const path = [];
    let actual = destinationId;
    while (actual !== sourceId) {
        path.push(actual);
        actual = previos[actual];
        if (!actual) return [];
    }
    path.push(sourceId);
    path.reverse();

    
    const resultado = [];
    let acumulado = 0;
    for (let i = 0; i < path.length; i++) {
        if (i === 0) {
            resultado.push({ id: path[i], distance: 0 });
        } else {
            const prev = path[i - 1];
            const curr = path[i];
            const salto = calculateDistance(graph[prev].connections[curr].price_usd);
            acumulado += salto;
            resultado.push({ id: curr, distance: acumulado });
        }
    }

    return resultado;
}


const filePath = path.resolve('c:/Users/mateo/Desktop/Semestre 8/Interactiva/IcesiGlobe/data/realistic_flight_graph.json');
const grafo = JSON.parse(fs.readFileSync(filePath, 'utf8'));

const camino = dijkstra(grafo, "133", "32");
console.log(camino);
