angular
    .module('restShopApp')
    .controller('HeaderController', HeaderController);

function HeaderController($location, $state, $window) {
    let vm = this;

    vm.searchProducts = searchProducts;
    vm.query = '';

    ////////////

    activate();

    function activate() {
        vm.query = $location.search().q || '';
    }
    function searchProducts() {
        $window.location.href = $state.href('product-list', {}, {absolute: true}) + '?q=' + vm.query;
    }
}
