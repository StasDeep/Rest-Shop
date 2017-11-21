angular
    .module('restShopApp')
    .controller('ProfileController', ProfileController);

function ProfileController($state, authDataService) {
    let vm = this;

    vm.active = {};
    vm.goToChild = goToChild;
    vm.logout = logout;
    vm.setActive = setActive;

    ////////////

    activate();

    function activate() {

    }

    function goToChild(state) {
        $state.go('profile.' + state);
    }

    function logout() {
        authDataService.logout();
        $state.go('product-list')
    }

    function setActive(state) {
        vm.active = {};
        vm.active[state] = true;
    }
}
