'use strict';


// Declare app level module which depends on filters, and services
angular.module('restShopApp', [
    'ui.router',
    'restShopApp.filters',
    'restShopApp.services',
    'restShopApp.directives',
    'restShopApp.controllers',
    'ngAnimate'
])
    .config(['$stateProvider',
        function ($stateProvider) {
            $stateProvider.state('sneakers', {
                url: '/sneakers',
                templateUrl: 'partials/sneakers.html',
                controller: 'SneakersCtrl'
            });
            $stateProvider.state('sneakers-details', {
                url: '/sneakers/:id',
                templateUrl: 'partials/sneakers-details.html',
                controller: 'SneakersDetailsCtrl'
            });
        }
    ])
    .run(function ($rootScope, $state) {
        $rootScope.$state = $state;
    });
