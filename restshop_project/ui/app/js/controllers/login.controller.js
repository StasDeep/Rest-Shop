angular
    .module('restShopApp')
    .controller('LoginController', LoginController);

function LoginController($state, authDataService) {
    let vm = this;

    vm.loginUser = loginUser;
    vm.email = '';
    vm.password = '';

    ////////////

    activate();

    function activate() {

    }

    function loginUser() {
        authDataService.login(vm.email, vm.password).then(function (response) {
            $state.go('product-list');
        });
    }
}
