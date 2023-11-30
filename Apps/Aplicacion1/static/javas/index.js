const container = document.querySelector('.container');
const aqiBox = document.querySelector('.aqi-box');
const aqiDetails = document.querySelector('.aqi-details');
const error404 = document.querySelector('.not-found');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

fetch(`/`, {
    method: 'GET',
    headers: {
        'X-CSFRToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
    }
})
    .then(
        function(response) {
            return response.json()
        }
    ).then(
        function(data) {
            console.log('xd')
        }
    )
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
        const pm25 = json.pm25;

        const image = document.querySelector('.aqi-box img');
        const temperature = document.querySelector('.aqi-box .temperature');
        const description = document.querySelector('.aqi-box .description');
        const humidity = document.querySelector('.aqi-details .humidity span');
        const wind = document.querySelector('.aqi-details .wind span');

        switch (json.description) {
            case 'Excelente':
                image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/wind_4515914.png';
                break;

            case 'Moderada':
                image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/2.png';
                break;

            case 'No saludables para grupos sensibles':
                image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/3.png';
                break;

            case 'Insalubre':
                image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/4.png';
                break;

            case 'Dañino':
                image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/5.png';
                break;

            case 'Muy Dañino':
                image.src = 'CATZ/Apps/Aplicacion1/static/imagenes/6.png';
                break;

            default:
                image.src = '';
        }

        temperature.innerHTML = `${parseInt(json.main.temp)}`;
        description.innerHTML = `${json.aqi[0].description}`;
        humidity.innerHTML = `${json.main.humidity}`;
        wind.innerHTML = `${parseInt(json.wind.speed)}`;

        aqiBox.style.display = '';
        aqiDetails.style.display = '';
        aqiBox.classList.add('fadeIn');
        aqiDetails.classList.add('fadeIn');
        container.style.height = '590px';
    });
