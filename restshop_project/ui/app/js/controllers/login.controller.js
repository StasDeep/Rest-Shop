angular
    .module('restShopApp')
    .controller('LoginController', LoginController);

function LoginController($state, authDataService) {
    let vm = this;

    vm.loginUser = loginUser;
    vm.user = {};

    ////////////

    activate();

    function activate() {

    }

    function loginUser() {
        authDataService.login(vm.user.email, vm.user.password).then(function (response) {
            $state.go('product-list');
        });
    }
}
