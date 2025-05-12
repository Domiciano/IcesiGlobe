const countryClickHandlers = {};

function onCountryClick(countryName, callback) {
  if (typeof callback === 'function') {
    countryClickHandlers[countryName] = callback;
  }
}

// Sobrescribe el evento general de clic en polígono
function enableEducationalCountryEvents() {
  world.onPolygonClick((feature) => {
    const id = countryNameToIdMap[feature.properties.name];
    const country = countriesData[id];
    const name = country.spanish_name;
    if (countryClickHandlers[name]) {
      countryClickHandlers[name](); // ejecuta la función registrada
    }
  });
}

function enableSolvedMode(){
  world.onPolygonClick((feature) => { 
    const id = countryNameToIdMap[feature.properties.name];
    const country = countriesData[id];
    const name = country.spanish_name;
    showCountryInfo(name);
  });

}
