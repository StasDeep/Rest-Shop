angular
    .module('restShopApp')
    .factory('cartOrderDataService', cartOrderDataService);

function cartOrderDataService(apiService) {
    let service = {
        addToCart: addToCart,
        deleteFromCart: deleteFromCart,
        getCart: getCart,
        getOrder: getOrder,
        getOrders: getOrders,
        createOrder: createOrder
    };

    return service;

    ////////////

    function addToCart(sku, quantity) {
        return apiService.post('cart', {sku: sku, quantity: quantity});
    }

    function deleteFromCart(sku) {
        return apiService.delete('cart', sku);
    }

    function getCart() {
        return apiService.get('cart').then((response) => {
            return response.data.data;
        });
    }

    function getOrder(id) {
        return apiService.get('orders', id).then((response) => {
            return response.data.data;
        });
    }

    function getOrders() {
        return apiService.get('orders').then((response) => {
            return response.data.data;
        });
    }

    function createOrder(name, address, phone) {
        return apiService.post('orders', {
            name: name,
            address: address,
            phone: phone
        });
    }
}
