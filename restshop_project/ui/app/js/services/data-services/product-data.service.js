angular
    .module('restShopApp')
    .factory('productDataService', productDataService);

function productDataService(apiService, orderingService) {
    let service = {
        getProduct: getProduct,
        getProducts: getProducts,
        getProperties: getProperties,
        getTags: getTags
    };

    return service;

    ////////////

    function getProduct(id) {
        return apiService.get('products', id).then((response) => {
            for (let unit of response.data.data.units) {
                if (unit.images.length == 0) {
                    unit.images.push(config.emptyImageUrl);
                }
            }

            return response.data.data;
        });
    }

    function getProducts(paramString) {
        return apiService.get('products', null, paramString).then((response) => {
            let items = response.data.data;

            for (let i = 0; i < items.length; i++) {
                if (items[i].image == null) {
                    items[i].image = config.emptyImageUrl;
                }
            }

            response.data.data = items;

            return response.data;
        });
    }

    function getProperties() {
        return apiService.get('properties').then((response) => {
            return orderingService.orderProperties(response.data.data);
        });
    }

    function getTags() {
        return apiService.get('tags').then((response) => {
            return orderingService.orderTags(response.data.data);
        });
    }
}
