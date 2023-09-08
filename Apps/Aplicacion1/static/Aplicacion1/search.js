mapboxgl.accessToken = 'pk.eyJ1IjoibXJpdmVybzAwIiwiYSI6ImNsbG11NWptbjF0ZmIzcXI2dDdybThnMmkifQ.uhdlXK3odioAdWo0OOogwA';

navigator.geolocation.getCurrentPosition(successLocation, erroLocation, { enableHighAccuracy: true });

function successLocation(position) {
    console.log(position)
    setupMap([position.coords.longitude, position.coords.latitude])
}

function erroLocation() {
    setupMap([-70.654191, -33.44395])
}

function setupMap(center) {
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: center,
    zoom: 15
  })
  
  const nav = new mapboxgl.NavigationControl();
  map.addControl(nav)

  var directions = new MapboxDirections({
    accessToken: mapboxgl.accessToken,
    language: 'es',
    unit: 'metric'
  });
  
  map.addControl(directions, 'top-left');
}