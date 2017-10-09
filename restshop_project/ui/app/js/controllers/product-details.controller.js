angular
    .module('restShopApp')
    .controller('ProductDetailsController', ProductDetailsController);

function ProductDetailsController($stateParams, $state, $window, productDataService, config, _) {
    let vm = this;

    vm.applyTag = applyTag;
    vm.colorItems = [];
    vm.loading = true;
    vm.options = [];
    vm.product = {};
    vm.selectedUnit = {};
    vm.setSelectedImage = setSelectedImage;
    vm.setSelectedUnit = setSelectedUnit;

    ////////////

    activate();

    function activate() {
        getProduct($stateParams.id);
    }

    function applyTag($event, tagName) {
        $event.stopPropagation();
        $window.location.href = $state.href('product-list', {}, {absolute: true}) + '?tags=' + tagName;
    }

    function getProduct(id) {
        productDataService.getProduct(id).then(function (product) {
            vm.product = product;
            vm.loading = false;
            setColorItems();
            setSelectedUnit(vm.colorItems[0].color);
        });
    }

    function setColorItems() {
        let colors = [];
        for (let i = 0; i < vm.product.units.length; i++) {
            let color;
            for (let j = 0; j < vm.product.units[i].properties.length; j++) {
                if (vm.product.units[i].properties[j].name == 'Color') {
                    color = vm.product.units[i].properties[j].value;
                    break;
                }
            }

            if (!colors.includes(color)) {
                colors.push(color);
                vm.colorItems.push({
                    color: color,
                    image: vm.product.units[i].images[0] || config.emptyImageUrl,
                    isSelected: false
                });
            }
        }
    }

    function setOptions() {

    }

    function setSelectedUnit(color) {
        for (let i = 0; i < vm.colorItems.length; i++) {
            vm.colorItems[i].isSelected = vm.colorItems[i].color === color;
        }

        let unitsWithColor = vm.product.units.filter(unit =>
            unit.properties.find(property =>
                property.name === 'Color'
            ).value === color
        );

        vm.selectedUnit = unitsWithColor[0];

        setSelectedImage(vm.selectedUnit.images[0]);
        setOptions();
    }

    function setSelectedImage(img) {
        vm.selectedUnit.img = img;
    }
}
