function handleGenerateArc() {

    const country1Select = document.getElementById("country1");
    const country2Select = document.getElementById("country2");
    const country1 = country1Select.value;
    const country2 = country2Select.value;
    const criteria = document.getElementById("criteria").value;



    if (!country1 || !country2 || country1 === country2) {
        alert("Selecciona dos países diferentes");
        return;
    }

    const id1 = countryNameToIdMap[country1];
    const id2 = countryNameToIdMap[country2];


    const path = dijkstraPath(flightGraph, id1, id2, criteria);

    if (!path.length) {
        alert("No existe una ruta entre estos países.");
        return;
    }

    let totalPrice = 0, totalDistance = 0, totalTime = 0, totalWeightedMetric = 0;
    arcsData = [];
    const routePoints = [];

    for (let i = 0; i < path.length - 1; i++) {
        const fromId = path[i];
        const toId = path[i + 1];
        const connection = flightGraph[fromId].connections[toId];

        totalPrice += connection.price_usd;

        const startLat = countriesData[fromId].lat;
        const startLon = countriesData[fromId].lon;
        const endLat = countriesData[toId].lat;
        const endLon = countriesData[toId].lon;

        if (startLat && startLon && endLat && endLon) {
            const startPoint = [startLon, startLat];
            const endPoint = [endLon, endLat];

            if (!routePoints.some(p => p[0] === startLon && p[1] === startLat)) {
                routePoints.push(startPoint);
            }
            if (!routePoints.some(p => p[0] === endLon && p[1] === endLat)) {
                routePoints.push(endPoint);
            }

            const distance = calculateHaversineDistance(startLat, startLon, endLat, endLon);
            totalDistance += distance;
            totalTime += connection.duration_hours;

            const weightedValue = calculateDistance(criteria, connection);
            totalWeightedMetric += weightedValue;

            arcsData.push({
                startLat,
                startLng: startLon,
                endLat,
                endLng: endLon,
                color: `hsl(${Math.random() * 360}, 70%, 50%)`,
            });
        }
    }

    world
        .arcsData(arcsData)
        .arcAltitudeAutoScale(0.5)
        .arcStroke(0.5)
        .arcDashLength(0.1)
        .arcDashGap(0.03)
        .arcDashAnimateTime(3000);

    const routeNames = new Set(path.map(id => idToCountryNameMap[id]));
    world.polygonCapColor(feature =>
        routeNames.has(feature.properties.name) ? "#386ee4" : "#183eb4"
    );

    centerGlobeView(routePoints);

    const country1Spanish = countryNamesToSpanish[country1] || country1;
    const country2Spanish = countryNamesToSpanish[country2] || country2;

    showTripInfo(country1Spanish, country2Spanish, totalPrice, totalDistance, path, criteria, totalWeightedMetric, totalTime);
}

function generateArc(lat1, lng1, lat2, lng2, color = 'orange') {
    const arc = {
        startLat: lat1,
        startLng: lng1,
        endLat: lat2,
        endLng: lng2,
        color: color
    };

    customArcs.push(arc); // 👈 acumula el arco

    world
        .arcsData(customArcs)
        .arcAltitudeAutoScale(0.5)
        .arcStroke(0.5)
        .arcDashLength(0.1)
        .arcDashGap(0.03)
        .arcDashAnimateTime(3000);
}
