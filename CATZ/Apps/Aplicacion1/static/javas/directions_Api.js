
mapboxgl.accessToken = "pk.eyJ1IjoibXJpdmVybzAwIiwiYSI6ImNsbG11NWptbjF0ZmIzcXI2dDdybThnMmkifQ.uhdlXK3odioAdWo0OOogwA"

// Coordenadas de inicio (Nueva York como ejemplo)
const startCoordinates = [-70.654191, -33.44395];

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: startCoordinates,
    zoom: 15,
});

// Obtener datos de calidad del aire de AQICN
const aqicnApiKey = '93467139e3a2fe6f3fb7d421d5d88ab634ef67d9';
const latitude = startCoordinates[1];
const longitude = startCoordinates[0];

const aqicnUrl = `https://api.waqi.info/feed/geo:${latitude};${longitude}/?token=${aqicnApiKey}`;

fetch(aqicnUrl)
    .then((response) => response.json())
    .then((data) => {
        const aqi = data.data.aqi;
        console.log(`Índice de Calidad del Aire (AQI): ${aqi}`);

        // Agregar un marcador con información de calidad del aire
        new mapboxgl.Marker({ color: getColorForAqi(aqi) })
            .setLngLat(startCoordinates)
            .setPopup(`AQI: ${aqi}`)
            .addTo(map);
    })
    .catch((error) => {
        console.error('Error al obtener datos de AQICN: ' + error);
    });

// Asocia un color a un nivel de AQI
function getColorForAqi(aqi) {
    if (aqi <= 50) {
        return 'green';
    } else if (aqi <= 100) {
        return 'yellow';
    } else {
        return 'red';
    }
}