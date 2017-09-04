'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
    'ui.router',
    'myApp.filters',
    'myApp.services',
    'myApp.directives',
    'myApp.controllers',
    'ngAnimate'
]).
config(['$stateProvider',
    function($stateProvider) {
        $stateProvider.state('sneakers', {
            url:'/sneakers',
            templateUrl: 'partials/sneakers.html',
            controller: 'SneakersCtrl'
        });
        $stateProvider.state('sneakers.details', {
            url:'/:id',
            templateUrl: 'partials/sneakers.details.html',
            controller: 'SneakersDetailsCtrl'
        });
    }
]);
