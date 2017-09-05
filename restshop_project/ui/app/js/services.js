'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', [])
    .constant('config', {
        serverUrl: 'http://localhost:8200',
        emptyImageUrl: 'img/empty.jpg'
    });
