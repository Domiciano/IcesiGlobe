document.addEventListener("DOMContentLoaded", () => {
    initGlobe();

    loadAppData().then((worldData) => {
        setupPolygons(worldData);
        populateCountrySelects(worldData);

        document.getElementById("generateArc").addEventListener("click", handleGenerateArc);
        document.getElementById("clearRoute").addEventListener("click", clearCurrentRoute);

        setupTouchInteractions();
        updateMobileUI();

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                clearCurrentRoute();
            }
        });
    });
});

window.addEventListener("resize", () => {
    if (arcsData.length > 0) {
        const routePoints = [];
        arcsData.forEach(arc => {
            const startPoint = [arc.startLng, arc.startLat];
            const endPoint = [arc.endLng, arc.endLat];

            if (!routePoints.some(p => p[0] === arc.startLng && p[1] === arc.startLat)) {
                routePoints.push(startPoint);
            }
            if (!routePoints.some(p => p[0] === arc.endLng && p[1] === arc.endLat)) {
                routePoints.push(endPoint);
            }
        });

        if (typeof centerGlobeView === 'function' && routePoints.length > 0) {
            centerGlobeView(routePoints);
        }
    }

    addMobileToggleButtons();
    updateMobileUI();
});
