angular
    .module('restShopApp')
    .controller('ProfileDeliveryInfoController', ProfileDeliveryInfoController);

function ProfileDeliveryInfoController($scope, userDataService) {
    let vm = this;

    vm.setDeliveryInfo = setDeliveryInfo;
    vm.deliveryInfo = {};

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive('deliveryInfo');

        userDataService.getDeliveryInfo().then((deliveryInfo) => {
            vm.deliveryInfo = deliveryInfo;
        });
    }

    function setDeliveryInfo() {
        userDataService.setDeliveryInfo(vm.deliveryInfo).then((response) => {
            // TODO: add logger notification.
        });
    }
}
