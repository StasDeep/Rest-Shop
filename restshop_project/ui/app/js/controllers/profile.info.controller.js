angular
    .module('restShopApp')
    .controller('ProfileInfoController', ProfileInfoController);

function ProfileInfoController($scope, userDataService) {
    let vm = this;

    vm.changePassword = changePassword;
    vm.password = {};

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive('info');
    }

    function changePassword() {
        userDataService.setPassword(vm.password.new).then((response) => {
            vm.password = {};
            // TODO: add logger notification.
        });
    }
}
