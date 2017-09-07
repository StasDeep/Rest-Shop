'use strict';

angular
    .module('restShopApp', [
        'ui.router',
        'ngAnimate'
    ])
    .config(['$stateProvider',
        function ($stateProvider) {
            $stateProvider.state('sneakers', {
                url: '/sneakers',
                templateUrl: 'partials/sneakers.html',
                controller: 'SneakersListController'
            });
            $stateProvider.state('sneakers-details', {
                url: '/sneakers/:id',
                templateUrl: 'partials/sneakers-details.html',
                controller: 'SneakersDetailsController'
            });
        }
    ])
    .run(function ($rootScope, $state) {
        $rootScope.$state = $state;
    });
