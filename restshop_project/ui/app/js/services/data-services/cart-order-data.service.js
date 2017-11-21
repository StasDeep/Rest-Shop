angular
    .module('restShopApp')
    .factory('cartOrderDataService', cartOrderDataService);

function cartOrderDataService($http, config) {
    let service = {
        addToCart: addToCart,
        getOrder: getOrder,
        getOrders: getOrders
    };

    return service;

    ////////////

    function addToCart(sku) {
        return $http.post(config.apiUrl + '/cart/', {sku: sku});
    }

    function getOrder(id) {
        return $http.get(config.apiUrl + '/orders/' + id + '/').then((response) => {
            return response.data.data;
        });
    }

    function getOrders() {
        return $http.get(config.apiUrl + '/orders/').then((response) => {
            return response.data.data;
        });
    }
}
