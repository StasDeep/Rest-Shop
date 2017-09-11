angular
    .module('restShopApp')
    .controller('SneakersDetailsController', SneakersDetailsController);

SneakersDetailsController.$inject = ['$stateParams', 'sneakersDataService'];

function SneakersDetailsController($stateParams, sneakersDataService) {
    var vm = this;

    vm.sneakers = {};

    ////////////

    activate();

    function activate() {
        getSneakersDetails($stateParams.id);
    }

    function getSneakersDetails(id) {
        sneakersDataService.getSneakersDetails(id);
    }
}
