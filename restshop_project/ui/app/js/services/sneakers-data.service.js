angular
    .module('restShopApp')
    .factory('sneakersDataService', sneakersDataService);

function sneakersDataService($http, config) {
    let service = {
        getProperties: getProperties,
        getSneakers: getSneakers,
        getSneakersDetails: getSneakersDetails,
        getTags: getTags
    };

    return service;

    ////////////

    function getProperties() {
        return $http.get(config.apiUrl + '/properties/').then(function (response) {
            return response.data;
        });
    }

    function getSneakers(paramString) {
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

    function getSneakersDetails(id) {
        return $http.get(config.apiUrl + '/products/' + id + '/').then(function (response) {
            return response.data;
        });
    }

    function getTags() {
        return $http.get(config.apiUrl + '/tags/').then(function (response) {
            return response.data;
        });
    }
}
