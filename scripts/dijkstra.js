function calculateDistance(type, conn) {
    if (type === 'precio') {
        return conn.price_usd;
    } else if (type === 'tiempo') {
        return conn.duration_hours;
    } else if (type === 'escalas') {
        return conn.hops;
    } else {
        throw new Error('Invalid cost type. Expected "precio", "tiempo" or "escalas".');
    }
}

function dijkstra(graph, sourceId, destinationId, cost) {
    const distances = {};
    const previos = {};
    const visited = new Set();
    const heap = [];

    for (const node in graph) {
        distances[node] = Infinity;
    }

    distances[sourceId] = 0;
    heap.push({ id: sourceId, distance: 0 });

    while (heap.length > 0) {
        heap.sort((a, b) => a.distance - b.distance);
        const { id: actualNode, distance: actualDistance } = heap.shift();

        if (visited.has(actualNode)) continue;
        visited.add(actualNode);

        if (actualNode === destinationId) break;

        const connections = graph[actualNode].connections;

        for (const neighborNode in connections) {
            const conn = connections[neighborNode];
            const weight = calculateDistance(cost, conn);
            const newDistance = actualDistance + weight;

            if (newDistance < distances[neighborNode]) {
                distances[neighborNode] = newDistance;
                previos[neighborNode] = actualNode;
                heap.push({ id: neighborNode, distance: newDistance });
            }
        }
    }

    if (distances[destinationId] === Infinity) return [];

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
            const conn = graph[prev].connections[curr];
            const salto = calculateDistance(cost, conn);
            acumulado += salto;
            resultado.push({ id: curr, distance: acumulado });
        }
    }

    return resultado;
}

function dijkstraPath(graph, sourceId, destinationId, cost) {
    const result = dijkstra(graph, sourceId, destinationId, cost);
    return result.map(item => item.id);
}
