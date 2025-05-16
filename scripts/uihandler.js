function getOptimizationName(type) {
  const names = {
    'precio': 'Menor precio',
    'tiempo': 'Menor tiempo',
    'escalas': 'Menos escalas'
  };
  return names[type] || type;
}

function showCountryInfo(countryName) {
  const name = countrySpanishNameToName[countryName];
  _showCountryInfo(name);
}

function _showCountryInfo(countryName) {
  const id = countryNameToIdMap[countryName];
  if (!id || !countriesData[id]) return;

  const country = countriesData[id];

  const modal = document.getElementById("countryModal");
  modal.innerHTML = `
    <div class="modal-header">
      ${country.spanish_name}
      <span class="modal-close">&times;</span>
    </div>
    <div class="modal-content">
      <div class="modal-section">
        <h4>Descripción</h4>
        <p>${country.info.description}</p>
      </div>
      
      <div class="modal-section">
        <h4>Clima</h4>
        <p>${country.info.climate}</p>
      </div>
      
      <div class="modal-section">
        <h4>Atracciones Turísticas</h4>
        <ul class="attraction-list">
          ${country.info.attractions.map(attraction => `<li>${attraction}</li>`).join('')}
        </ul>
      </div>
      
      <div class="modal-section">
        <h4>Curiosidades</h4>
        <ul class="curiosity-list">
          ${country.info.curiosities.map(curiosity => `<li>${curiosity}</li>`).join('')}
        </ul>
      </div>
    </div>
  `;
  modal.style.display = "block";

  modal.querySelector(".modal-close").addEventListener("click", () => {
    modal.style.display = "none";
  });
}

function addMobileToggleButtons() {
  if (window.innerWidth <= 768) {
    const tripInfo = document.getElementById("tripInfo");
    if (tripInfo && tripInfo.style.display === "block") {
      let toggleBtn = document.querySelector('.mobile-toggle-info');
      if (!toggleBtn) {
        toggleBtn = document.createElement('div');
        toggleBtn.className = 'mobile-toggle-info';
        toggleBtn.innerHTML = '↕️';
        toggleBtn.title = 'Expandir/Contraer información';
        document.body.appendChild(toggleBtn);

        let isExpanded = true;

        toggleBtn.addEventListener('click', () => {
          if (isExpanded) {
            tripInfo.style.maxHeight = '80px';
            tripInfo.style.overflow = 'hidden';
            toggleBtn.innerHTML = '↓';
          } else {
            tripInfo.style.maxHeight = 'calc(60vh - 20px)';
            tripInfo.style.overflow = 'auto';
            toggleBtn.innerHTML = '↕️';
          }
          isExpanded = !isExpanded;
        });
      }
    } else {
      const existingBtn = document.querySelector('.mobile-toggle-info');
      if (existingBtn) {
        existingBtn.remove();
      }
    }
  }
}

function showTripInfo(from, to, price, distance, path, criteria, weightedMetric, flightTime) {
  const infoBox = document.getElementById("tripInfo");
  const flightTimeString = flightTime.toFixed(1);

  const stops = path.map((id) => {
    const engName = idToCountryNameMap[id];
    return countryNamesToSpanish[engName] || engName;
  }).join(" → ");

  let optimizedBy = getOptimizationName(criteria);

  let optimizationDetails = "";

  if (criteria === 'precio') {
    optimizationDetails = `
      <p class="optimization-detail">
        <small>Valor optimizado: $${weightedMetric.toFixed(2)} USD</small>
      </p>
    `;
  } else if (criteria === 'tiempo') {
    optimizationDetails = `
      <p class="optimization-detail">
        <small>Valor optimizado: ${weightedMetric.toFixed(2)} horas</small>
      </p>
    `;
  } else if (criteria === 'escalas') {
    optimizationDetails = `
      <p class="optimization-detail">
        <small>Valor optimizado: ${path.length - 1} escalas</small>
      </p>
    `;
  }

  infoBox.innerHTML = `
    <div class="trip-info-header">
      Información del Viaje
    </div>
    <div class="trip-info-content">
      <div class="trip-info-section">
        <h3>Detalles del Itinerario</h3>
        <p><strong>Origen:</strong> ${from}</p>
        <p><strong>Destino:</strong> ${to}</p>
        <p><strong>Optimización:</strong> ${optimizedBy} <span class="trip-info-badge">Ruta óptima</span></p>
        ${optimizationDetails}
      </div>
      
      <div class="trip-info-section">
        <h3>Ruta del Viaje</h3>
        <div class="trip-info-route">
          ${stops}
        </div>
        <p><small>La ruta pasa por ${path.length} países con ${path.length - 2} escalas</small></p>
      </div>
      
      <div class="trip-info-section">
        <h3>Métricas del Viaje</h3>
        <div class="trip-info-metrics">
          <div class="trip-info-metric">
            <div class="metric-value">$${price.toFixed(2)}</div>
            <div class="metric-label">USD</div>
          </div>
          <div class="trip-info-metric">
            <div class="metric-value">${distance.toFixed(0)}</div>
            <div class="metric-label">kilómetros</div>
          </div>ACCC
          <div class="trip-info-metric">
            <div class="metric-value">${flightTimeString}</div>
            <div class="metric-label">horas de vuelo</div>
          </div>
          <div class="trip-info-metric">
            <div class="metric-value">${path.length - 2}</div>
            <div class="metric-label">escalas</div>
          </div>
        </div>
      </div>
      
      <button id="closeTripInfo">Cerrar</button>
    </div>
  `;

  infoBox.style.display = "block";

  document.getElementById("closeTripInfo").addEventListener("click", () => {
    infoBox.style.display = "none";
    const toggleBtn = document.querySelector('.mobile-toggle-info');
    if (toggleBtn) toggleBtn.remove();
  });

  addMobileToggleButtons();
}

function updateMobileUI() {
  const isMobile = window.innerWidth < 768 || /Mobi|Android/i.test(navigator.userAgent);

  if (isMobile) {
    document.body.classList.add('mobile-device');
  } else {
    document.body.classList.remove('mobile-device');
  }
}

function clearCurrentRoute() {
  const country1Select = document.getElementById("country1");
  const country2Select = document.getElementById("country2");
  country1Select.selectedIndex = 0;
  country2Select.selectedIndex = 0;

  const tripInfo = document.getElementById("tripInfo");
  tripInfo.style.display = "none";

  const countryModal = document.getElementById("countryModal");
  countryModal.style.display = "none";

  if (world) {
    world.arcsData([]);
    world.polygonCapColor(() => "#183eb4");
    world.pointOfView({ lat: 0, lng: 0, altitude: 2.5 }, 1000);
  }

  arcsData = [];
}

function centerGlobeView(points) {
  if (!points || points.length === 0) return;

  if (points.length === 1) {
    const [lng, lat] = points[0];
    world.pointOfView({ lat, lng, altitude: 2.5 }, 1000);
    return;
  }

  let sumLat = 0, sumLng = 0;
  points.forEach(point => {
    sumLng += point[0];
    sumLat += point[1];
  });

  const avgLng = sumLng / points.length;
  const avgLat = sumLat / points.length;

  let maxDist = 0;
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      const startPoint = turf.point(points[i]);
      const endPoint = turf.point(points[j]);
      const dist = turf.distance(startPoint, endPoint);
      maxDist = Math.max(maxDist, dist);
    }
  }

  const altitude = Math.max(1.5, Math.min(4, 1.5 + maxDist / 5000));

  world.pointOfView({ lat: avgLat, lng: avgLng, altitude }, 1000);
}

function populateCountrySelects(worldData) {
  let countryNames = [];

  if (worldData.features && worldData.features.length > 0) {
    countryNames = worldData.features.map((f) => f.properties.name).sort();
  } else {
    countryNames = Object.values(countriesData).map(country => country.name).sort();
  }

  const country1Select = document.getElementById("country1");
  const country2Select = document.getElementById("country2");

  country1Select.innerHTML = '<option value="" disabled selected>País de origen</option>';
  country2Select.innerHTML = '<option value="" disabled selected>País de destino</option>';

  countryNames.forEach((name) => {
    const spanishName = countryNamesToSpanish[name] || name;

    const option1 = document.createElement('option');
    option1.value = name;
    option1.textContent = spanishName;
    country1Select.appendChild(option1);

    const option2 = document.createElement('option');
    option2.value = name;
    option2.textContent = spanishName;
    country2Select.appendChild(option2);
  });
}
