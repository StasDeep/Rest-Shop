angular
    .module('restShopApp')
    .constant('config', {
        apiUrl: 'http://localhost:8000/api',
        emptyImageUrl: '/static/img/empty.png'
    })
    .constant('_', window._)
    .config(configCsrf);

function configCsrf($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}

