angular
    .module('restShopApp')
    .controller('ProfileDeliveryInfoController', ProfileDeliveryInfoController);

function ProfileDeliveryInfoController($scope, userDataService, notifier) {
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
            notifier.success('Successfully changed delivery info');
        }, (response) => {
            notifier.error('Cannot change delivery info');
        });
    }
}
