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
                translate: (value, sliderId, label) => {
                    switch (label) {
                        case 'model':
                            return 'Min: $' + value;
                        case 'high':
                            return 'Max: $' + value;
                        default:
                            return '$' + value
                    }
                },
                onEnd: () => {
                    refreshFilter();
                }
            }
        };
    }

    function getInitializedProperties() {
        return productDataService.getProperties().then((properties) => {
            let propertiesFromUrl = $location.search().properties || '';
            propertiesFromUrl = propertiesFromUrl.split(',');

            return properties.map((property) => {
                property.values.map((value) => {
                    let idsForValue = property.mapping[value.value];
                    let allIdsInUrl = idsForValue.filter(id => !propertiesFromUrl.includes(id.toString())).length == 0;
                    let anyId = idsForValue.length > 0;
                    value.selected = anyId && allIdsInUrl;

                    return value;
                });
                return property;
            });
        });
    }

    function getInitializedTags() {
        return productDataService.getTags().then((tags) => {
            let tagsFromUrl = $location.search().tags || '';
            tagsFromUrl = tagsFromUrl.split(',').map((tag) => {
                return tag.toLowerCase()
            });

            return tags.map((tag) => {
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

        productDataService.getProducts(paramString).then((data) => {
            vm.hasNext = data.meta.has_next;
            vm.hasPrev = data.meta.has_prev;
            vm.page = data.meta.page;
            vm.products = data.data;
            vm.loading = false;

            initializeSlider(data.meta.min_price, data.meta.max_price);
        });
    }

    function initializeFilterValues() {
        getInitializedTags().then((tags) => {
            vm.tags = tags;
        });

        getInitializedProperties().then((properties) => {
            vm.properties = properties;
        });

        vm.inStock = $location.search().in_stock == '1';
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
        let selectedTags = vm.tags.filter(tagObj => tagObj.selected).map(tagObj => tagObj.name);

        let tagsParamValue = selectedTags.join(',') || null;
        addFilterParam('tags', tagsParamValue);

        let selectedProperties = [];
        for (let prop of vm.properties) {
            for (let value of prop.values) {
                if (value.selected) {
                    selectedProperties.push(...prop.mapping[value.value]);
                }
            }
        }
        let propertiesParamValue = selectedProperties.join(',') || null;
        addFilterParam('properties', propertiesParamValue);

        let inStockParamValue = vm.inStock ? '1' : null;
        addFilterParam('in_stock', inStockParamValue);

        if (vm.slider.min == vm.slider.options.floor) {
            addFilterParam('price_min', null);
        } else {
            addFilterParam('price_min', vm.slider.min.toString())
        }

        if (vm.slider.max == vm.slider.options.ceil) {
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
