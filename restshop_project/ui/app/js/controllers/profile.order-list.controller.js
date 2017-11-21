angular
    .module('restShopApp')
    .controller('ProfileOrderListController', ProfileOrderListController);

function ProfileOrderListController($scope, cartOrderDataService) {
    let vm = this;

    vm.orders = [];
    vm.loading = true;

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive('orders');

        cartOrderDataService.getOrders().then((orders) => {
            vm.orders = orders;
            vm.loading = false;
        });
    }
}
