angular
    .module('restShopApp')
    .factory('sneakersDataService', sneakersDataService);

sneakersDataService.$inject = ['$http', 'urlParamsService', 'config'];

function sneakersDataService($http, urlParamsService, config) {
    var service = {
        getProperties: getProperties,
        getSneakers: getSneakers,
        getSneakersDetails: getSneakersDetails,
        getTags: getTags
    };

    return service;

    ////////////

    function getProperties() {
        return $http.get(config.serverUrl + '/properties/').then(function (response) {
            return response.data;
        });
    }

    function getSneakers() {
        var apiPath = config.serverUrl + '/products/';
        var paramString = urlParamsService.getParamString(['tags', 'properties']);
        var url = apiPath + paramString;

        return $http.get(url).then(function (response) {
            var items = response.data.results;

            for (var i = 0; i < items.length; i++) {
                if (items[i].image === null) {
                    items[i].image = config.emptyImageUrl;
                } else {
                    items[i].image = config.serverUrl + items[i].image;
                }
            }

            response.data.results = items;

            return response.data;
        });
    }

    function getSneakersDetails(id) {
        return $http.get(config.serverUrl + '/products/' + id).then(function (response) {
            return response.data;
        });
    }

    function getTags() {
        return $http.get(config.serverUrl + '/tags/').then(function (response) {
            return response.data;
        });
    }
}
