angular
    .module('restShopApp', [
        'ui.router',
        'ngAnimate',
        'ui.bootstrap',
        'rzModule',
        'cgNotify'
    ])
    .config(routeConfig)
    .run(addUserToRootScope)
    .run(addAuthorization);

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
        .state('cart', {
            url: '/cart',
            templateUrl: '/static/partials/cart.html',
            controller: 'CartController',
            controllerAs: 'vm'
        })
        .state('profile', {
            url: '/profile',
            templateUrl: '/static/partials/profile.html',
            controller: 'ProfileController',
            controllerAs: 'vm',
            data: {
                isAuthenticated: true
            }
        })
        .state('profile.info', {
            url: '/info',
            templateUrl: '/static/partials/profile.info.html',
            controller: 'ProfileInfoController',
            controllerAs: 'vm'
        })
        .state('profile.delivery-info', {
            url: '/delivery-info',
            templateUrl: '/static/partials/profile.delivery-info.html',
            controller: 'ProfileDeliveryInfoController',
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

function addUserToRootScope($rootScope, userDataService) {
    $rootScope.user = null;
    $rootScope.isLogged = () => !!$rootScope.user;
    $rootScope.userPromise = userDataService.setUser();
}

function addAuthorization($rootScope, $state) {
    $rootScope.$on('$stateChangeStart', (event, toState, toParams, fromState, fromParams) => {
        $rootScope.userPromise.then(() => {
            if (needAuthentication(toState) && !$rootScope.isLogged()) {
                event.preventDefault();
                $state.go('login')
            }
        });
    });
}

function needAuthentication(state) {
    if (state.data && state.data.isAuthenticated) {
        return true;
    } else if (state.parent) {
        return needAuthentication(state.parent);
    } else {
        return false;
    }
}
