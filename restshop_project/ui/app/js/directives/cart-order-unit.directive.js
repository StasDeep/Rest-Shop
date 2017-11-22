angular
    .module('restShopApp')
    .directive('rsCartOrderUnit', cartOrderUnit);

function cartOrderUnit() {
    let directive = {
        restrict: 'E',
        templateUrl: '/static/partials/cart-order-unit.html',
        scope: {
            item: '=',
            isCart: '<',
            onQuantityChange: '&'
        },
        controller: cartOrderUnitController,
        controllerAs: 'vm',
        bindToController: true
    };

    return directive;
}

function cartOrderUnitController($scope) {
    let vm = this;

    vm.onQuantityClick = onQuantityClick;
    vm.onQuantityContainerClick = onQuantityContainerClick;
    vm.toggleHover = toggleHover;
    vm.quantityHovered = false;

    ////////////

    function onQuantityClick($event, change) {
        $event.preventDefault();
        $event.stopPropagation();

        vm.onQuantityChange({$change: change});
    }

    function onQuantityContainerClick($event) {
        $event.preventDefault();
        $event.stopPropagation();
    }

    function toggleHover(type) {
        vm.quantityHovered = type == 'enter';
    }
}
