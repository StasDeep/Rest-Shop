angular
    .module('restShopApp')
    .controller('ProductDetailsController', ProductDetailsController);

function ProductDetailsController($stateParams, $state, $window, $timeout, productDataService, cartOrderDataService,
                                  propertiesTagService, _, notifier) {
    let vm = this;

    vm.addToCart = addToCart;
    vm.applyOption = applyOption;
    vm.applyTag = applyTag;
    vm.colorMap = {};
    vm.price = undefined;
    vm.isChosen = isChosen;
    vm.loading = true;
    vm.product = {};
    vm.selectedImage = null;
    vm.selectedOptions = [];
    vm.thumbnails = [];
    vm.setSelectedImage = setSelectedImage;

    ////////////

    activate();

    function activate() {
        getProduct($stateParams.id).then(() => {
            initColorMap();
            setSelectedUnit();
            initOptions();
            setOptionsWidth();
            setAllowedOptions();
            setPrice();
        });
    }

    function addToCart() {
        let selectedSku = getMatchingUnit().sku;
        cartOrderDataService.addToCart(selectedSku).then((response) => {
            notifier.success('Successfully added to cart');
        });
    }

    function applyOption(property, value) {
        // Set value to property, if not set. Otherwise, reset value.
        let option = vm.selectedOptions.find(p => p.name == property);
        option.selected = option.selected != value ? value : null;

        setAllowedOptions();
        setSelectedUnit(getMatchingUnit());
        setPrice();
    }

    function applyTag($event, tagName) {
        $event.stopPropagation();
        $window.location.href = $state.href('product-list', {}, {absolute: true}) + '?tags=' + encodeURIComponent(tagName);
    }

    function getMatchingUnit() {
        let selectedProperties = vm.selectedOptions.filter(p => p.selected != null);

        return vm.product.units.find(unit => {
            for (let selectedProp of selectedProperties) {
                let unitProp = unit.properties.find(p => p.name == selectedProp.name);

                if (unitProp.value != selectedProp.selected) {
                    return false;
                }
            }

            return true;
        });
    }

    function getMatchingUnits(filterProperties) {
        if (_.isUndefined(filterProperties)) {
            filterProperties = vm.selectedOptions.filter(p => p.selected != null);
        }

        return vm.product.units.filter(unit => {
            if (unit.num_in_stock == 0) {
                return false;
            }

            for (let selectedProp of filterProperties) {
                let unitProp = unit.properties.find(p => p.name == selectedProp.name);

                if (unitProp.value != selectedProp.selected) {
                    return false;
                }
            }

            return true;
        });
    }

    function getProduct(id) {
        return productDataService.getProduct(id).then((product) => {
            vm.product = product;
            vm.loading = false;
        });
    }

    function getPropertyValue(unit, propertyName) {
        return unit.properties.find(p => p.name == propertyName).value;
    }

    function getUnitPrice() {
        let prices = getMatchingUnits().map(unit => unit.price);
        if (prices.length == 0) {
            return '';
        }

        let minPrice = Math.min(...prices);
        let maxPrice = Math.max(...prices);

        if (minPrice == maxPrice) {
            return '$' + minPrice;
        } else {
            return '$' + minPrice + ' - ' + '$' + maxPrice;
        }
    }

    function initColorMap() {
        for (let unit of vm.product.units) {
            let color = getPropertyValue(unit, 'Color');

            if (!_.keys(vm.colorMap).includes(color)) {
                vm.colorMap[color] = unit.images[0];
            }
        }
    }

    function initOptions() {
        for (let prop of vm.product.units[0].properties) {
            let options = [];

            for (let unit of vm.product.units) {
                let value = getPropertyValue(unit, prop.name);
                if (!options.map(opt => opt.value).includes(value)) {
                    options.push({
                        value: value,
                        allowed: true
                    });
                }
            }

            vm.selectedOptions.push({
                name: prop.name,
                selected: null,
                options: options
            })
        }

        vm.selectedOptions = propertiesTagService.orderProperties(vm.selectedOptions, 'options');
    }

    function isChosen() {
        return vm.selectedOptions.filter(p => p.selected == null).length == 0;
    }

    function setAllowedOptions() {
        let selectedProperties = vm.selectedOptions.filter(p => p.selected != null);

        for (let prop of vm.selectedOptions) {
            let filterProperties = selectedProperties.filter(p => p.name != prop.name);
            let allowedValues = _.uniq(getMatchingUnits(filterProperties)
                                       .map(unit => getPropertyValue(unit, prop.name)));

            for (let option of prop.options) {
                option.allowed = allowedValues.includes(option.value);
            }
        }
    }

    function setOptionsWidth() {
        $timeout(() => {
            angular.forEach(document.querySelectorAll('.options-row'), row => {
                let maxWidth = 0;
                let optionElements = row.querySelectorAll('.option-container');

                angular.forEach(optionElements, elem => {
                    let width = elem.clientWidth;
                    let border = angular.element(elem).css('border-width');

                    if (width > maxWidth) {
                        maxWidth = width + 2 * border;
                    }
                });

                maxWidth += 2; // For a border

                angular.forEach(optionElements, elem => {
                    angular.element(elem).css('width', maxWidth + 'px');
                });
            });
        });
    }

    function setPrice() {
        vm.price = getUnitPrice();
    }

    function setSelectedUnit(unit) {
        unit = unit || vm.product.units[0];

        let imgIndex = vm.thumbnails.indexOf(vm.selectedImage);

        vm.thumbnails = unit.images;
        setSelectedImage(vm.thumbnails[imgIndex] || vm.thumbnails[0]);
    }

    function setSelectedImage(img) {
        vm.selectedImage = img;
    }
}
