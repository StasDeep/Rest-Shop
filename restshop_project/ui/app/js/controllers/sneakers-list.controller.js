angular
    .module('restShopApp')
    .controller('SneakersListController', SneakersListController);

function SneakersListController($location, $anchorScroll, urlParamsService, sneakersDataService) {
    let vm = this;

    vm.addFilterParam = addFilterParam;
    vm.applyTag = applyTag;
    vm.getSneakers = getSneakers;
    vm.hasNext = false;
    vm.hasPrev = false;
    vm.loading = true;
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

        getSneakers();
    }

    function addFilterParam(param, value) {
        urlParamsService.addParam(param, value);
    }

    function applyTag($event, tagName) {
        $event.stopPropagation();

        for (let i = 0; i < vm.tags.length; i++) {
            vm.tags[i].selected = vm.tags[i].name.toLowerCase() === tagName.toLowerCase();
        }

        refreshFilter();
    }

    function getInitializedProperties() {
        return sneakersDataService.getProperties().then(function (properties) {
            let propertiesFromUrl = $location.search().properties || '';
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
            let tagsFromUrl = $location.search().tags || '';
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

    function getSneakers() {
        vm.loading = true;

        sneakersDataService.getSneakers().then(function (data) {
            vm.hasNext = data.has_next;
            vm.hasPrev = data.has_prev;
            vm.page = data.page;
            vm.sneakersListing = data.results;
            vm.loading = false;
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

    function pageNext() {
        addFilterParam('page', vm.page + 1);
        getSneakers();

        // Scroll to top of the page to show new results.
        $anchorScroll();
    }

    function pagePrev() {
        addFilterParam('page', vm.page - 1);
        getSneakers();

        // Scroll to top of the page to show new results.
        $anchorScroll();
    }

    function refreshFilter() {
        let selectedTags = vm.tags
            .filter(function (tagObj) {
                return tagObj.selected;
            })
            .map(function (tagObj) {
                return tagObj.name;
            });

        let tagsParamValue = selectedTags.join(',') || null;
        addFilterParam('tags', tagsParamValue);

        let selectedProperties = [];
        for (let i = 0; i < vm.properties.length; i++) {
            for (let j = 0; j < vm.properties[i].values.length; j++) {
                if (vm.properties[i].values[j].selected) {
                    selectedProperties.push(vm.properties[i].values[j].id)
                }
            }
        }
        let propertiesParamValue = selectedProperties.join(',') || null;
        addFilterParam('properties', propertiesParamValue);

        let inStockParamValue = vm.inStock ? '1' : null;
        addFilterParam('in_stock', inStockParamValue);

        let priceMinParamValue = vm.priceMin ? vm.priceMin.toString() : null;
        addFilterParam('price_min', priceMinParamValue);

        let priceMaxParamValue = vm.priceMax ? vm.priceMax.toString() : null;
        addFilterParam('price_max', priceMaxParamValue);

        getSneakers();
    }
}
