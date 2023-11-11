const container = document.querySelector('.container');
const aqiBox = document.querySelector('.aqi-box');
const aqiDetails = document.querySelector('.aqi-details');
const error404 = document.querySelector('.not-found');

fetch(`/recibir_ubicacion/`)
    .then(response => response.json())
    .then(json => {
        
        if (json.cod === '404') {
            container.style.height = '400px';
            aqiBox.style.display = 'none';
            aqiDetails.style.display = 'none';
            error404.style.display = 'block';
            error404.classList.add('fadeIn');
            return;
        }

        error404.style.display = 'none';
        error404.classList.remove('fadeIn');

        const aqi = json.aqi;
        const res = json.res;
        const pm10 = json.pm10;
        const co = json.co;

        const image = document.querySelector('.aqi-box img');
        const temperature = document.querySelector('.aqi-box .temperature');
        const description = document.querySelector('.aqi-box .description');
        const humidity = document.querySelector('.aqi-details .humidity span');
        const wind = document.querySelector('.aqi-details .wind span');

    });

    switch (json.description) {
        case 'Excelente':
            image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/wind_4515914.png';
            break;

        case 'Moderada':
            image.src = 'images/rain.png';
            break;

        case 'Snow':
            image.src = 'images/snow.png';
            break;

        case 'Clouds':
            image.src = 'images/cloud.png';
            break;

        case 'Haze':
            image.src = 'images/mist.png';
            break;

        default:
            image.src = '';
    }
