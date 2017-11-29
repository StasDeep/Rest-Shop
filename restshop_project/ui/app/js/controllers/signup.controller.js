angular
    .module('restShopApp')
    .controller('SignupController', SignupController);

function SignupController(userDataService, notifier) {
    let vm = this;

    vm.signup = signup;
    vm.successfullySigned = false;
    vm.user = {};

    ////////////

    activate();

    function activate() {

    }

    function signup() {
        userDataService.signup(vm.user.email, vm.user.password).then((response) => {
            vm.successfullySigned = true;
        }, (response) => {
            if (response.data.error.email) {
                if (response.data.error.email[0] == 'Enter a valid email address.') {
                    notifier.error('There is no such email address')
                } else {
                    notifier.error('Email is already taken');
                }
            } else {
                notifier.error('Cannot create new account');
            }
        });
    }
}
