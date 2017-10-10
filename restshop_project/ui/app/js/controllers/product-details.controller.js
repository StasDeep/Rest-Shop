angular
    .module('restShopApp')
    .controller('ProductDetailsController', ProductDetailsController);

function ProductDetailsController($stateParams, $state, $window, $timeout, productDataService, _) {
    let vm = this;

    vm.applyOption = applyOption;
    vm.applyTag = applyTag;
    vm.colorMap = {};
    vm.loading = true;
    vm.selectedOptions = [];
    vm.product = {};
    vm.selectedImage = null;
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
        });
    }

    function applyOption(property, value) {

    }

    function applyTag($event, tagName) {
        $event.stopPropagation();
        $window.location.href = $state.href('product-list', {}, {absolute: true}) + '?tags=' + tagName;
    }

    function getProduct(id) {
        return productDataService.getProduct(id).then(function (product) {
            vm.product = product;
            vm.loading = false;
        });
    }

    function initColorMap() {
        for (let unit of vm.product.units) {
            let color = getPropertyValue(unit, 'Color');

            if (!_.keys(vm.colorMap).includes(color)) {
                vm.colorMap[color] = unit.images[0];
            }
        }
    }

    function getPropertyValue(unit, propertyName) {
        return unit.properties.find((p) => p.name === propertyName).value;
    }

    function initOptions() {
        for (let prop of vm.product.units[0].properties) {
            let options = [];

            for (let unit of vm.product.units) {
                let value = getPropertyValue(unit, prop.name);
                if (!options.map((opt) => opt.value).includes(value)) {
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
    }

    function setOptionsWidth() {
        $timeout(() => {
            angular.forEach(document.querySelectorAll('.options-row'), (row) => {
                let maxWidth = 0;
                let optionElements = row.querySelectorAll('.option-container');

                angular.forEach(optionElements, (elem) => {
                    let width = elem.clientWidth;
                    let border = angular.element(elem).css('border-width');

                    if (width > maxWidth) {
                        maxWidth = width + 2 * border;
                    }
                });

                maxWidth += 2; // For a border

                angular.forEach(optionElements, (elem) => {
                    angular.element(elem).css('width', maxWidth + 'px');
                });
            });
        });
    }

    function setSelectedUnit(unit) {
        unit = unit || vm.product.units[0];

        vm.thumbnails = unit.images;
        setSelectedImage(vm.thumbnails[0]);
    }

    function setSelectedImage(img) {
        vm.selectedImage = img;
    }
}
