angular
    .module('restShopApp')
    .controller('SignupController', SignupController);

function SignupController($state, userDataService) {
    let vm = this;

    vm.signup = signup;
    vm.successfullySigned = false;
    vm.user = {};

    ////////////

    activate();

    function activate() {

    }

    function signup() {
        userDataService.signup(vm.user.email, vm.user.password).then(function (response) {
            vm.successfullySigned = true;
        });
    }
}
