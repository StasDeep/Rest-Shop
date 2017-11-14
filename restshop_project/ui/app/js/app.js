angular
    .module('restShopApp', [
        'ui.router',
        'ngAnimate',
        'ui.bootstrap',
        'rzModule'
    ])
    .config(routeConfig)
    .run(addStateToRootScope)
    .run(addUserToRootScope);

function routeConfig($stateProvider, $locationProvider, $urlRouterProvider) {
    $stateProvider
        .state('product-list', {
            url: '/products',
            templateUrl: '/static/partials/product-list.html',
            controller: 'ProductListController',
            controllerAs: 'vm'
        })
        .state('product-details', {
            url: '/products/:id',
            templateUrl: '/static/partials/product-details.html',
            controller: 'ProductDetailsController',
            controllerAs: 'vm'
        })
        .state('login', {
            url: '/login',
            templateUrl: '/static/partials/login.html',
            controller: 'LoginController',
            controllerAs: 'vm'
        });

    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });

    $urlRouterProvider.otherwise(function ($injector) {
        let $state = $injector.get('$state');
        $state.go('product-list');
    });
}

function addStateToRootScope($rootScope, $state) {
    $rootScope.$state = $state;
}

function addUserToRootScope($rootScope, authDataService) {
    $rootScope.user = null;
    authDataService.setUser();
}
