// Ejercicio 1
// Ubicar a Colombia
addMarker(3, -76, 'Cali, Colombia');
addMarker(0, 0, 'Cali, Colombia');
addMarker(10, 10, 'Cali, Colombia');

//Ejercicio 2
// Crear un arco con el lugar a donde le gustaría viajar
generateArc(3.4516, -76.5320, 0, 0);

//Ejercicio 3
//Acción al dar click sobre algun pais
onCountryClick("Colombia", () => {
    alert("Has dado click a Colombia");
    showCountryInfo("Colombia");
});

//Ejercicio 4
//Obtener el arreglo de djisktra e imprimir en alert lat y lng de [0], [1], ...
path = dijkstra("Colombia", "Egipto");
lat0 = path[0].latitude;
lon0 = path[0].longitude;

lat1 = path[1].latitude;
lon1 = path[1].longitude;

lat2 = path[2].latitude;
lon2 = path[2].longitude;

//alert(lat0)
//alert(lon0)

//Ejercicio 5
//Conectar arcos dados por dijkstra
generateArc(lat0, lon0, lat1, lon1);
generateArc(lat1, lon1, lat2, lon2);

//Ejercicio 6
doTheMagic();
