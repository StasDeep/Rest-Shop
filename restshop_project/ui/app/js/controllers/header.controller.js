angular
    .module('restShopApp')
    .controller('HeaderController', HeaderController);

function HeaderController($location, $state, $window) {
    let vm = this;

    vm.navigateToSneakers = navigateToSneakers;
    vm.query = '';

    ////////////

    activate();

    function activate() {
        vm.query = $location.search().q || '';
    }

    function navigateToSneakers() {
        $window.location.href = $state.href('sneakers', {}, {absolute: true}) + '?q=' + vm.query;
    }
}
