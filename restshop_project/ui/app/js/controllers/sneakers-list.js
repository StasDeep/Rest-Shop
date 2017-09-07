angular
    .module('restShopApp')
    .controller('SneakersListController', SneakersListController);

SneakersListController.$inject = ['$scope', '$http', '$location', '$anchorScroll', 'config'];

function SneakersListController($scope, $http, $location, $anchorScroll, config) {
    function addUrlParameter(parameter, value) {
        // Reset page, because list can become smaller and thus page can no longer exist.
        $location.search('page', null);
        $location.search(parameter, value);
    }

    $scope.addUrlParameterAndReloadList = function (parameter, value) {
        addUrlParameter(parameter, value);
        $scope.loadList()
    };

    function getQueryString() {
        var queryString = '?';

        var q = $location.search().q;
        var page = $location.search().page;
        var inStock = $location.search().in_stock;
        var tags = $location.search().tags;
        var properties = $location.search().properties;
        var priceMin = $location.search().price_min;
        var priceMax = $location.search().price_max;

        if (q) {
            queryString += 'q=' + q + ';';
        }
        if (page) {
            queryString += 'page=' + page + ';';
        }
        if (inStock) {
            queryString += 'in_stock=' + inStock + ';';
        }
        if (priceMin) {
            queryString += 'price_min=' + priceMin + ';';
        }
        if (priceMax) {
            queryString += 'price_max=' + priceMax + ';';
        }
        if (tags) {
            tags = tags.split(',');

            for (var i = 0; i < tags.length; i++) {
                queryString += 'tags=' + tags[i] + ';';
            }
        }
        if (properties) {
            properties = properties.split(',');

            for (var i = 0; i < properties.length; i++) {
                queryString += 'properties=' + properties[i] + ';';
            }
        }

        return queryString;
    }

    $scope.loadList = function () {
        var apiPath = config.serverUrl + '/products/';

        $http.get(apiPath + getQueryString()).then(function (response) {
            var items = response.data.results;

            for (var i = 0; i < items.length; i++) {
                if (items[i].image === null) {
                    items[i].image = config.emptyImageUrl;
                } else {
                    items[i].image = config.serverUrl + items[i].image;
                }
            }

            $scope.sneakersListing = items;
            $scope.page = response.data.page;
            $scope.hasPrev = response.data.has_prev;
            $scope.hasNext = response.data.has_next;

            // Scroll to top of the page to show new results.
            $anchorScroll();
        });
    };

    $scope.refreshFilter = function () {
        var selectedTags = $scope.tags
            .filter(function (tagObj) {
                return tagObj.selected;
            })
            .map(function (tagObj) {
                return tagObj.name;
            });

        var tagsParamValue = selectedTags.join(',') || null;
        addUrlParameter('tags', tagsParamValue);

        var selectedProperties = [];
        for (var i = 0; i < $scope.properties.length; i++) {
            for (var j = 0; j < $scope.properties[i].values.length; j++) {
                if ($scope.properties[i].values[j].selected) {
                    selectedProperties.push($scope.properties[i].values[j].id)
                }
            }
        }
        var propertiesParamValue = selectedProperties.join(',') || null;
        addUrlParameter('properties', propertiesParamValue);

        var inStockParamValue = $scope.inStock ? '1' : null;
        addUrlParameter('in_stock', inStockParamValue);

        var priceMinParamValue = $scope.priceMin ? $scope.priceMin.toString() : null;
        addUrlParameter('price_min', priceMinParamValue);

        var priceMaxParamValue = $scope.priceMax ? $scope.priceMax.toString() : null;
        addUrlParameter('price_max', priceMaxParamValue);

        $scope.loadList();
    };

    $http.get(config.serverUrl + '/tags/').then(function (response) {
        var tagsFromUrl = $location.search().tags || '';
        tagsFromUrl = tagsFromUrl.split(',').map(function (tag) {
            return tag.toLowerCase()
        });

        $scope.tags = response.data.map(function (tag) {
            var isSelected = tagsFromUrl.includes(tag.toLowerCase());
            return {
                name: tag,
                selected: isSelected
            }
        });
    });

    $http.get(config.serverUrl + '/properties/').then(function (response) {
        var propertiesFromUrl = $location.search().properties || '';
        propertiesFromUrl = propertiesFromUrl.split(',');

        $scope.properties = response.data.map(function (property) {
            property.values.map(function (value) {
                value.selected = propertiesFromUrl.includes(value.id.toString());
                return value;
            });
            return property;
        });
    });

    $scope.inStock = $location.search().in_stock === '1';

    $scope.priceMin = $location.search().price_min;
    $scope.priceMin = parseInt($scope.priceMin);

    $scope.priceMax = $location.search().price_max;
    $scope.priceMax = parseInt($scope.priceMax);

    $scope.loadList();
}
