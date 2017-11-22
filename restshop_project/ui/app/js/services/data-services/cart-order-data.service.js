angular
    .module('restShopApp')
    .factory('cartOrderDataService', cartOrderDataService);

function cartOrderDataService($http, config) {
    let service = {
        addToCart: addToCart,
        deleteFromCart: deleteFromCart,
        getCart: getCart,
        getOrder: getOrder,
        getOrders: getOrders
    };

    return service;

    ////////////

    function addToCart(sku, quantity) {
        return $http.post(config.apiUrl + '/cart/', {sku: sku, quantity: quantity});
    }

    function deleteFromCart(sku) {
        return $http.delete(config.apiUrl + '/cart/' + sku + '/');
    }

    function getCart() {
        return $http.get(config.apiUrl + '/cart/').then((response) => {
            return response.data.data;
        });
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
