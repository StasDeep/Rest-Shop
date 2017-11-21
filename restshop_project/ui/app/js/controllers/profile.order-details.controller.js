angular
    .module('restShopApp')
    .controller('ProfileOrderDetailsController', ProfileOrderDetailsController);

function ProfileOrderDetailsController($scope, $stateParams, cartOrderDataService) {
    let vm = this;

    vm.order = {};
    vm.loading = true;

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive(null);

        cartOrderDataService.getOrder($stateParams.id).then((order) => {
            vm.order = order;
            vm.loading = false;
        });
    }
}
