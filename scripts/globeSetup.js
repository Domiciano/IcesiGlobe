// Inicializa el globo 3D y lo asigna a la variable global `world`
function initGlobe() {
    world = Globe()
        .globeImageUrl("./assets/water-texture.png")
        .backgroundImageUrl("./assets/night-sky.png")
        .backgroundColor("black")(document.getElementById("globeViz"));
}

function setupTouchInteractions() {
    document.getElementById('globeViz').addEventListener('touchmove', function (e) {
        if (e.touches.length > 1) {
            e.preventDefault();
        }
    }, { passive: false });

    window.addEventListener('orientationchange', function () {
        setTimeout(() => {
            if (arcsData.length > 0) {
                const routePoints = [];
                arcsData.forEach(arc => {
                    const startPoint = [arc.startLng, arc.startLat];
                    const endPoint = [arc.endLng, arc.endLat];

                    const startExists = routePoints.some(p => p[0] === arc.startLng && p[1] === arc.startLat);
                    const endExists = routePoints.some(p => p[0] === arc.endLng && p[1] === arc.endLat);

                    if (!startExists) routePoints.push(startPoint);
                    if (!endExists) routePoints.push(endPoint);
                });

                if (typeof centerGlobeView === 'function' && routePoints.length > 0) {
                    centerGlobeView(routePoints);
                }
            }
        }, 300); r
    });
}
function setupPolygons(worldData) {
    world
        .polygonsData(worldData.features)
        .polygonCapColor(() => "#183eb4")
        .polygonSideColor(() => "rgba(0, 0, 0, 0.0)")
        .polygonStrokeColor(() => "#020a73")
        //.onPolygonClick((feature) => _showCountryInfo(feature.properties.name));
}

function addMarker(lat, lng, label = '') {
    const marker = {
      lat: lat,
      lng: lng,
      size: 0.5,
      color: 'white',
      label: label
    };
  
    // Si ya hay otros puntos, mantenlos. Si no, inicia con este.
    const existingPoints = world.pointsData() || [];
    world.pointsData([...existingPoints, marker])
         .pointAltitude('size')
         .pointColor('color')
         .pointLabel('label');
  }
  