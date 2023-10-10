const ACCESS_TOKEN = 'pk.eyJ1IjoibXJpdmVybzAwIiwiYSI6ImNsbG11NWptbjF0ZmIzcXI2dDdybThnMmkifQ.uhdlXK3odioAdWo0OOogwA';

mapboxgl.accessToken = ACCESS_TOKEN;
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-70.654191, -33.44395],
  zoom: 9,
});

const script = document.createElement('script');
script.id = 'search-js';
script.src = 'https://api.mapbox.com/search-js/v1.0.0-beta.17/web.js';
script.defer = true;
document.head.appendChild(script);

script.onload = function () {
  const searchBox = new MapboxSearchBox();
  searchBox.accessToken = ACCESS_TOKEN;
  searchBox.options = {
    types: 'address,poi,place,locality',
    proximity: [-70.654191, -33.44395],
    language: 'es'
  };
  searchBox.marker = true;
  searchBox.mapboxgl = mapboxgl;
  map.addControl(searchBox);
};
