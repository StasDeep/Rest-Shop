angular
    .module('restShopApp')
    .controller('SneakersListController', SneakersListController);

SneakersListController.$inject = ['$location', '$anchorScroll', 'urlParamsService', 'sneakersDataService'];

function SneakersListController($location, $anchorScroll, urlParamsService, sneakersDataService) {
    var vm = this;

    vm.addFilterParam = addFilterParam;
    vm.hasNext = false;
    vm.hasPrev = false;
    vm.loadList = loadList;
    vm.page = 1;
    vm.pageNext = pageNext;
    vm.pagePrev = pagePrev;
    vm.properties = [];
    vm.refreshFilter = refreshFilter;
    vm.sneakersListing = [];
    vm.tags = [];

    ////////////

    activate();

    function activate() {
        // Reset page on each param adding.
        urlParamsService.setResetParams(['page']);

        initializeFilterValues();

        loadList();
    }

    function addFilterParam(param, value) {
        urlParamsService.addParam(param, value);
    }

    function getInitializedProperties() {
        return sneakersDataService.getProperties().then(function (properties) {
            var propertiesFromUrl = $location.search().properties || '';
            propertiesFromUrl = propertiesFromUrl.split(',');

            return properties.map(function (property) {
                property.values.map(function (value) {
                    value.selected = propertiesFromUrl.includes(value.id.toString());
                    return value;
                });
                return property;
            });
        });
    }

    function getInitializedTags() {
        return sneakersDataService.getTags().then(function (tags) {

            var tagsFromUrl = $location.search().tags || '';
            tagsFromUrl = tagsFromUrl.split(',').map(function (tag) {
                return tag.toLowerCase()
            });

            return tags.map(function (tag) {
                return {
                    name: tag,
                    selected: tagsFromUrl.includes(tag.toLowerCase())
                }
            });
        });
    }

    function initializeFilterValues() {
        getInitializedTags().then(function (tags) {
            vm.tags = tags;
        });

        getInitializedProperties().then(function (properties) {
            vm.properties = properties;
        });

        vm.inStock = $location.search().in_stock === '1';

        vm.priceMin = $location.search().price_min;
        vm.priceMin = parseInt(vm.priceMin);

        vm.priceMax = $location.search().price_max;
        vm.priceMax = parseInt(vm.priceMax);
    }

    function loadList() {
        sneakersDataService.getSneakers().then(function (data) {
            vm.hasNext = data.has_next;
            vm.hasPrev = data.has_prev;
            vm.page = data.page;
            vm.sneakersListing = data.results;
        });
    }

    function pageNext() {
        addFilterParam('page', vm.page + 1);
        loadList();

        // Scroll to top of the page to show new results.
        $anchorScroll();
    }

    function pagePrev() {
        addFilterParam('page', vm.page - 1);
        loadList();

        // Scroll to top of the page to show new results.
        $anchorScroll();
    }

    function refreshFilter() {
        var selectedTags = vm.tags
            .filter(function (tagObj) {
                return tagObj.selected;
            })
            .map(function (tagObj) {
                return tagObj.name;
            });

        var tagsParamValue = selectedTags.join(',') || null;
        addFilterParam('tags', tagsParamValue);

        var selectedProperties = [];
        for (var i = 0; i < vm.properties.length; i++) {
            for (var j = 0; j < vm.properties[i].values.length; j++) {
                if (vm.properties[i].values[j].selected) {
                    selectedProperties.push(vm.properties[i].values[j].id)
                }
            }
        }
        var propertiesParamValue = selectedProperties.join(',') || null;
        addFilterParam('properties', propertiesParamValue);

        var inStockParamValue = vm.inStock ? '1' : null;
        addFilterParam('in_stock', inStockParamValue);

        var priceMinParamValue = vm.priceMin ? vm.priceMin.toString() : null;
        addFilterParam('price_min', priceMinParamValue);

        var priceMaxParamValue = vm.priceMax ? vm.priceMax.toString() : null;
        addFilterParam('price_max', priceMaxParamValue);

        loadList();
    }
}
