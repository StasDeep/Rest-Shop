angular
    .module('restShopApp')
    .controller('ProfileOrderDetailsController', ProfileOrderDetailsController);

function ProfileOrderDetailsController($scope, $stateParams, cartOrderDataService) {
    let vm = this;

    vm.getTotalSum = getTotalSum;
    vm.loading = true;
    vm.order = {};

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive(null);

        cartOrderDataService.getOrder($stateParams.id).then((order) => {
            vm.order = order;
            vm.loading = false;
        });
    }

    function getTotalSum() {
        return vm.order.units.map(ou => ou.quantity * ou.unit.price).reduce((a, b) => a + b, 0);
    }
}
