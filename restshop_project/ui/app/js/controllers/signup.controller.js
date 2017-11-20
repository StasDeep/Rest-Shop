angular
    .module('restShopApp')
    .controller('SignupController', SignupController);

function SignupController($state, authDataService) {
    let vm = this;

    vm.signup = signup;
    vm.successfullySigned = false;
    vm.user = {};

    ////////////

    activate();

    function activate() {

    }

    function signup() {
        authDataService.signup(vm.user.email, vm.user.password).then(function (response) {
            vm.successfullySigned = true;
        });
    }
}
