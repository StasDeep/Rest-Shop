angular
    .module('restShopApp')
    .factory('sneakersDataService', sneakersDataService);

sneakersDataService.$inject = ['$http', 'urlParamsService', 'config'];

function sneakersDataService($http, urlParamsService, config) {
    var service = {
        getList: getList
    };

    return service;

    ////////////

    function getList() {
        var apiPath = config.serverUrl + '/products/';
        var paramString = urlParamsService.getParamString(['tags', 'properties']);
        var url = apiPath + paramString;

        var promise = $http.get(url).then(function (response) {
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

        return promise;
    }
}
