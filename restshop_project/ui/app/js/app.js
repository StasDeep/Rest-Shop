angular
    .module('restShopApp', [
        'ui.router',
        'ngAnimate'
    ])
    .config(['$stateProvider',
        function ($stateProvider) {
            $stateProvider.state('sneakers', {
                url: '/sneakers',
                templateUrl: 'partials/sneakers-list.html',
                controller: 'SneakersListController',
                controllerAs: 'vm'
            });
            $stateProvider.state('sneakers-details', {
                url: '/sneakers/:id',
                templateUrl: 'partials/sneakers-details.html',
                controller: 'SneakersDetailsController',
                controllerAs: 'vm'
            });
        }
    ])
    .run(function ($rootScope, $state) {
        $rootScope.$state = $state;
    });
