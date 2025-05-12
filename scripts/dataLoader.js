function loadAppData() {
    return Promise.all([
      fetch("data/countries.json").then(res => res.json()),
      fetch("data/realistic_flight_graph.json").then(res => res.json()),
      fetch("data/world_with_ids.json").then(res => res.json())
    ]).then(([countries, graph, worldData]) => {
      countriesData = countries;
      flightGraph = graph;
  
      Object.keys(countriesData).forEach(id => {
        const name = countriesData[id].name;
        const spanish_name = countriesData[id].spanish_name;
        countryNameToIdMap[name] = id;
        countrySpanishNameToName[spanish_name] = name;
        idToCountryNameMap[id] = name;
        countryNamesToSpanish[name] = countriesData[id].spanish_name;
        if (countriesData[id].lat && countriesData[id].lon) {
          countryCentroids[name] = [countriesData[id].lon, countriesData[id].lat];
        }
      });
      return worldData;
    });
  }
  