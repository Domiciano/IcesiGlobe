Goals

[CONTEXTO CON IA Icesi Global Internacional]

En presentación explicamos las coordenadas geodésicas. La proyección Mercator vs la vista esférica.

- Ejercicio 1: Ubicar un marcador sobre Icesi

En presentación explicamos los arcos

- Ejercicio 2: Crear un arco entre Icesi y el lugar al que sueñan viajar


En la presentacion explicar variables

- Ejercicio 3: Obtener el nombre de los paises al clcik


En presentación explicamos un grafo minimalista a escala de los paises

En presentación explicamos Djikstra como algoritmo para minimizar costo de recorrido

En la presentacion explicar los arreglos

- Ejercicio 4: Obtener el arreglo de djisktra e imprimir en alert lat y lng de [0], [1], ...

- Ejercicio 5: Crear arcos manualmente
- Ejercicio 5 Alternativo: Crear arcos por medio de for

- Ejercicio FINAL: Boton que haga todo




Tareas:
- Dijkstra y arreglo de caminos
Mateo Silva
- Data de adyacencias de paises realista (Puentes aereos) (IA), precio y tiempo de vuelo. Crear estrcutura para comunicarla a Dijkstra. world.json tiene que tener ID de pais y información del pais, una descripción del país con enfoque de turista
Kevin Nieto
- Front
Mariana, Gabriel y Juan Camilo


Para esto tenemos que tener la app desarrollada
- Abstraccion para los aspirantes
- Presentación e instrucciones
---

# Estructura de los archivos JSON utilizados en ICESI Interactiva

Este documento describe la estructura, el objetivo y las consideraciones especiales de los principales archivos JSON utilizados en el proyecto **ICESI Interactiva**.

---

## 1. countries.json

```json
{
  "1": {
    "name": "Afghanistan",
    "spanish_name": "Afganistán",
    "info": {
      "description": "Afganistán está dominado por la cordillera del Hindu Kush y posee una historia que abarca imperios persas, mogoles y soviéticos.",
      "climate": "Clima continental extremo con veranos secos y calurosos e inviernos fríos; en las montañas las nevadas son abundantes.",
      "attractions": [
        "Ciudadela de Herat",
        "Minarete y yacimiento arqueológico de Jam (UNESCO)",
        "Lago Band‑e Amir en Bamiyán",
        "Mercados tradicionales de Kabul"
      ],
      "curiosities": [
        "El buzkashi, un juego ecuestre de origen nómada, es considerado el deporte nacional.",
        "Fue un importante tramo de la antigua Ruta de la Seda."
      ]
    },
    "lat": 33.7680065,
    "lon": 66.2385139
  },
...
}
```

**Características:**
- Cada clave corresponde al **ID** numérico del país.
- Contiene los siguientes atributos:
  - `name`: Nombre oficial en inglés (usado para integraciones, APIs y queries).
  - `spanish_name`: Nombre en español (usado para presentaciones en la interfaz).
  - `info`: Objeto con información turística:
    - `description`, `climate`, `attractions`, `curiosities`, todos en **español**.
  - `lat`: latitud del país.
  - `lon`: longitud del país.


**Notas:**
- Toda la información turística fue generada con inteligencia artificial para aumentar la precisión y riqueza de detalles.

> **Importante:** Para integrar con APIs como [Nominatim](https://nominatim.openstreetmap.org/), siempre debes utilizar el atributo `name` y **no** `spanish_name`, ya que todos los `name` fueron validados con la api con el script `scripts/verifyCountry.py`.

---

## 2. realistic_flight_graph.json

Este archivo representa el **grafo de vuelos realistas** entre países.

**Origen de los datos:**
- Basado en la base de datos abierta de **OpenFlights** del cual se tomó las rutas y aeropuertos registrado en la IATA.
- Datos de aeropuertos (`graphData/airports.dat`) y rutas directas (`graphData/routes.dat`).

**Cálculos:**
- **Distancia:** Usando la fórmula de **Haversine** entre las coordenadas de los aeropuertos que contiene la propia base de datos de airports.dat.
- **Duración:** `distancia / 900 km/h` (promedio estimado de velocidad de vuelo).
- **Precio:** `50 USD + 0.10 USD/km`.

**Estructura:**
```json
{
  "1": {
    "country_name": "Afghanistan",
    "connections": {
      "33": {
        "country_name": "China",
        "duration_hours": 6.5,
        "price_usd": 400.0,
        "hops": 0
      },
      ...
    }
  },
  ...
}
```

- Las claves principales son los **IDs** de `countries.json`.
- Cada nodo incluye su `country_name` para facilidad de lectura.
- Dentro de `connections`, cada destino también incluye su `country_name` y atributos de la conexión.

**Validaciones:**
- Se implementó un algoritmo de **Dijkstra** básico para verificar rutas y optimizaciones, este algoritmo se encuentra en `scripts/testDijkstra.py` con la documentación para ejecutarlo.
- Se puede priorizar por:
  - `duration_hours` (tiempo de vuelo)
  - `price_usd` (costo total)
  - `hops` (cantidad de escalas)

**Restricciones:**
- Sólo se consideran rutas **directas** encontradas en `routes.dat`.

---

## 3. world_with_ids.json

Este archivo contiene las **geometrías** de cada país (polígonos para renderizado en mapas) junto con el **ID** asociado.

**Estructura:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Afghanistan",
        "id": 1
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [...]
      }
    },
    ...
  ]
}
```
---

### Implemetacion de Dijkstra

se creo el archivo `dijkstra.js` el cual ya contiene el archivo que se quiere para poder usarlo en la aplicacion, ¿como usarlo?

```js
const filePath = path.resolve('your/path');
const grafo = JSON.parse(fs.readFileSync(filePath, 'utf8'));

const camino = dijkstra(grafo, "133", "32") // el primer numero es el origen y el segundo el destino, revisa que esten en el grafo para probar;
console.log(camino) //por si lo quiere probar;
```

**Notas:**
- Cada `Feature` tiene un `properties.name` (nombre del país) y un `properties.id` (ID de `countries.json`).
- El `id` actúa como **clave primaria** para todas las operaciones cruzadas entre los JSON.

---

# Resumen
- **name**: Atributo base para integraciones externas.
- **spanish_name**: Uso interno y visual.
- **id**: Clave primaria en todos los archivos.

