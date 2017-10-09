angular
    .module('restShopApp')
    .controller('ProductListController', ProductListController);

function ProductListController($location, productDataService) {
    let vm = this;

    vm.hasNext = false;
    vm.hasPrev = false;
    vm.loading = true;
    vm.page = 1;
    vm.pageNext = pageNext;
    vm.pagePrev = pagePrev;
    vm.properties = [];
    vm.products = [];
    vm.refreshFilter = refreshFilter;
    vm.slider = getDefaultSlider();
    vm.tags = [];

    ////////////

    activate();

    function activate() {
        initializeFilterValues();
        getProducts();
    }

    function addFilterParam(param, value) {
        $location.search(param, value);
    }

    function getDefaultSlider() {
        return {
            min: 0,
            max: 995,
            options: {
                floor: 0,
                ceil: 995,
                noSwitching: true,
                step: 5,
                translate: function (value, sliderId, label) {
                    switch (label) {
                        case 'model':
                            return 'Min: $' + value;
                        case 'high':
                            return 'Max: $' + value;
                        default:
                            return '$' + value
                    }
                },
                onEnd: function () {
                    refreshFilter();
                }
            }
        };
    }

    function getInitializedProperties() {
        return productDataService.getProperties().then(function (properties) {
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
        return productDataService.getTags().then(function (tags) {
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

    function getProducts() {
        vm.loading = true;

        // Query parameters in URL are the same as parameters for API request
        // that is why we can request API with this query string.
        let paramString = $location.url().split('?')[1] || '';

        productDataService.getProducts(paramString).then(function (data) {
            vm.hasNext = data.has_next;
            vm.hasPrev = data.has_prev;
            vm.page = data.page;
            vm.products = data.results;
            vm.loading = false;

            initializeSlider(data.min_price, data.max_price);
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
    }

    function initializeSlider(floor, ceil) {
        let min = parseInt($location.search().price_min) || 0;
        if (min < floor || min > ceil) {
            min = floor;
        }

        let max = parseInt($location.search().price_max) || 1000;
        if (max < floor || max > ceil) {
            max = ceil;
        }

        vm.slider.min = min;
        vm.slider.max = max;
        vm.slider.options.floor = floor;
        vm.slider.options.ceil = ceil;
    }

    function pageNext() {
        addFilterParam('page', vm.page + 1);
        getProducts();
    }

    function pagePrev() {
        addFilterParam('page', vm.page - 1);
        getProducts();
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

        if (vm.slider.min === vm.slider.options.floor) {
            addFilterParam('price_min', null);
        } else {
            addFilterParam('price_min', vm.slider.min.toString())
        }

        if (vm.slider.max === vm.slider.options.ceil) {
            addFilterParam('price_max', null);
        } else {
            addFilterParam('price_max', vm.slider.max.toString())
        }

        // Reset page, because filtering can decrease num of pages
        // and current page number can become invalid.
        addFilterParam('page', null);

        getProducts();
    }
}
