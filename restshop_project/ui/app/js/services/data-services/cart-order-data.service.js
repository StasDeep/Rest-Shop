angular
    .module('restShopApp')
    .factory('cartOrderDataService', cartOrderDataService);

/* @ngInject */
function cartOrderDataService($http, config) {
    let service = {
        addToCart: addToCart
    };

    return service;

    ////////////

    function addToCart(sku) {
        return $http.post(config.apiUrl + '/cart/', {sku: sku});
    }
}
