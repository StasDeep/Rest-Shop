angular
    .module('restShopApp')
    .controller('LoginController', LoginController);

function LoginController($state, userDataService, notifier) {
    let vm = this;

    vm.loginUser = loginUser;
    vm.user = {};

    ////////////

    activate();

    function activate() {

    }

    function loginUser() {
        userDataService.login(vm.user.email, vm.user.password).then((response) => {
            $state.go('product-list');
        }, (response) => {
            notifier.error('Wrong email or password');
        });
    }
}
