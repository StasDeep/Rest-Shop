angular
    .module('restShopApp')
    .controller('ProductDetailsController', ProductDetailsController);

function ProductDetailsController($stateParams, productDataService) {
    let vm = this;

    vm.loading = true;
    vm.product = {};

    ////////////

    activate();

    function activate() {
        getProduct($stateParams.id);
    }

    function getProduct(id) {
        productDataService.getProduct(id).then(function (product) {
            vm.product = product;
            vm.loading = false;
        });
    }
}
