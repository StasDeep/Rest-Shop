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
        })
        .state('signup', {
            url: '/signup',
            templateUrl: '/static/partials/signup.html',
            controller: 'SignupController',
            controllerAs: 'vm'
        })
        .state('profile', {
            url: '/profile',
            templateUrl: '/static/partials/profile.html',
            controller: 'ProfileController',
            controllerAs: 'vm'
        })
        .state('profile.info', {
            url: '/info',
            templateUrl: '/static/partials/profile.info.html',
            controller: 'ProfileInfoController',
            controllerAs: 'vm'
        })
        .state('profile.order-list', {
            url: '/orders',
            templateUrl: '/static/partials/profile.order-list.html',
            controller: 'ProfileOrderListController',
            controllerAs: 'vm'
        })
        .state('profile.order-details', {
            url: '/orders/:id',
            templateUrl: '/static/partials/profile.order-details.html',
            controller: 'ProfileOrderDetailsController',
            controllerAs: 'vm'
        });

    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });

    $urlRouterProvider.otherwise(($injector) => {
        let $state = $injector.get('$state');
        $state.go('product-list');
    });
}

function addStateToRootScope($rootScope, $state) {
    $rootScope.$state = $state;
}

function addUserToRootScope($rootScope, authDataService) {
    $rootScope.user = null;
    $rootScope.isLogged = () => !!$rootScope.user;
    authDataService.setUser();
}
