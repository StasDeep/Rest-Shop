angular
    .module('restShopApp')
    .controller('ProfileInfoController', ProfileInfoController);

function ProfileInfoController($scope, userDataService, notifier) {
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
            notifier.success('Successfully changed password');
        }, (response) => {
            notifier.error('Cannot change password');
        });
    }
}
