angular
    .module('restShopApp')
    .factory('productDataService', productDataService);

function productDataService($http, orderingService, config) {
    let service = {
        getProduct: getProduct,
        getProducts: getProducts,
        getProperties: getProperties,
        getTags: getTags
    };

    return service;

    ////////////

    function getProduct(id) {
        return $http.get(config.apiUrl + '/products/' + id + '/').then(function (response) {
            for (let unit of response.data.data.units) {
                if (unit.images.length == 0) {
                    unit.images.push(config.emptyImageUrl);
                }
            }

            return response.data.data;
        });
    }

    function getProducts(paramString) {
        let apiPath = config.apiUrl + '/products/';
        let url = apiPath + '?' + paramString;

        return $http.get(url).then(function (response) {
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
        return $http.get(config.apiUrl + '/properties/').then(function (response) {
            return orderingService.orderProperties(response.data.data);
        });
    }

    function getTags() {
        return $http.get(config.apiUrl + '/tags/').then(function (response) {
            return orderingService.orderTags(response.data.data);
        });
    }
}
