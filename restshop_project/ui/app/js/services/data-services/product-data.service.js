angular
    .module('restShopApp')
    .factory('productDataService', productDataService);

function productDataService(apiService, propertiesTagService, config) {
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
            return propertiesTagService.filterProperties(response.data.data);
        });
    }

    function getTags() {
        return apiService.get('tags').then((response) => {
            return propertiesTagService.orderTags(response.data.data);
        });
    }
}
