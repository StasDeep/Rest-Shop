angular
    .module('restShopApp')
    .controller('SneakersDetailsController', SneakersDetailsController);

SneakersDetailsController.$inject = ['$http', '$stateParams', 'config'];

function SneakersDetailsController($http, $stateParams, config) {
    var vm = this;

    vm.sneakers = {};

    ////////////

    $http.get(config.serverUrl + '/products/' + $stateParams.id).then(function (response) {
        vm.sneakers = response.data;
    });
}
