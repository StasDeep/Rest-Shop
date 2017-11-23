angular
    .module('restShopApp')
    .controller('ProfileInfoController', ProfileInfoController);

function ProfileInfoController($scope, authDataService) {
    let vm = this;

    vm.changePassword = changePassword;
    vm.password = {};

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive('info');
    }

    function changePassword() {
        authDataService.setPassword(vm.password.new).then((response) => {
            console.log('Successfully changed');
        });
    }
}
