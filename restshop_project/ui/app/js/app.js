angular
    .module('restShopApp', [
        'ui.router',
        'ngAnimate'
    ])
    .config(routeConfig)
    .run(addStateToRootScope);

function routeConfig($stateProvider, $locationProvider, $urlRouterProvider, $injector) {
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

function addStateToRootScope($rootScope, $state) {
    $rootScope.$state = $state;
}
