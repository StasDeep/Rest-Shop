angular
    .module('restShopApp')
    .controller('SneakersDetailsController', SneakersDetailsController);

SneakersDetailsController.$inject = ['$scope', '$http', '$stateParams', 'config']

function SneakersDetailsController($scope, $http, $stateParams, config) {
    $scope.id = $stateParams.id;

    $http.get(config.serverUrl + '/products/' + $scope.id).then(function (response) {
        $scope.sneakers = response.data;
    });
}
