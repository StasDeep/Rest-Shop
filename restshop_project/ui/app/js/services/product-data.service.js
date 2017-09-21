angular
    .module('restShopApp')
    .factory('productDataService', productDataService);

function productDataService($http, config) {
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
            return response.data;
        });
    }

    function getProducts(paramString) {
        let apiPath = config.apiUrl + '/products/';
        let url = apiPath + '?' + paramString;

        return $http.get(url).then(function (response) {
            let items = response.data.results;

            for (let i = 0; i < items.length; i++) {
                if (items[i].image === null) {
                    items[i].image = config.emptyImageUrl;
                }
            }

            response.data.results = items;

            return response.data;
        });
    }

    function getProperties() {
        return $http.get(config.apiUrl + '/properties/').then(function (response) {
            return response.data;
        });
    }

    function getTags() {
        return $http.get(config.apiUrl + '/tags/').then(function (response) {
            return response.data;
        });
    }
}
