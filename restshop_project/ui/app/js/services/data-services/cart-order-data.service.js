angular
    .module('restShopApp')
    .factory('cartOrderDataService', cartOrderDataService);

/* @ngInject */
function cartOrderDataService($http, config) {
    let service = {
        addToCart: addToCart,
        getOrders: getOrders
    };

    return service;

    ////////////

    function addToCart(sku) {
        return $http.post(config.apiUrl + '/cart/', {sku: sku});
    }

    function getOrders() {
        return $http.get(config.apiUrl + '/orders/').then((response) => {
            return response.data.data;
        });
    }
}
