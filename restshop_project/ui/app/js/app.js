angular
    .module('restShopApp', [
        'ui.router',
        'ngAnimate'
    ])
    .config(['$stateProvider', '$locationProvider', '$urlRouterProvider', '$injector',
        function ($stateProvider, $locationProvider, $urlRouterProvider, $injector) {
            $stateProvider
                .state('sneakers', {
                    url: '/sneakers',
                    templateUrl: '/static/partials/sneakers-list.html',
                    controller: 'SneakersListController',
                    controllerAs: 'vm'
                })
                .state('sneakers-details', {
                    url: '/sneakers/:id',
                    templateUrl: '/static/partials/sneakers-details.html',
                    controller: 'SneakersDetailsController',
                    controllerAs: 'vm'
                });

            $locationProvider.html5Mode({
              enabled: true,
              requireBase: false
            });

            $urlRouterProvider.otherwise(function ($injector) {
                var $state = $injector.get('$state');
                $state.go('sneakers');
            });
        }
    ])
    .run(function ($rootScope, $state) {
        $rootScope.$state = $state;
    });
