angular
    .module('restShopApp')
    .controller('ProfileInfoController', ProfileInfoController);

function ProfileInfoController($scope, authDataService) {
    let vm = this;

    vm.user = {};

    ////////////

    activate();

    function activate() {
        $scope.vm.setActive('info');
    }
}
