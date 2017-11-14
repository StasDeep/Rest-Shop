angular
    .module('restShopApp')
    .controller('HeaderController', HeaderController);

function HeaderController($location, $rootScope, $state, $window, authDataService) {
    let vm = this;

    vm.logout = logout;
    vm.searchProducts = searchProducts;
    vm.query = '';

    ////////////

    activate();

    function activate() {
        vm.query = $location.search().q || '';
    }

    function logout() {
        authDataService.logout();
    }

    function searchProducts() {
        $window.location.href = $state.href('product-list', {}, {absolute: true}) + '?q=' + vm.query;
    }
}
