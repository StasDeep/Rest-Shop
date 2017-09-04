'use strict';
angular.module('myApp.controllers', [])
    .controller('SneakersCtrl', ['$scope', '$http', '$location', function($scope, $http, $location) {
        $scope.go = function (path) {
            $location.path(path);
        };

        $http.get('http://localhost:8200/products/').then(function (response) {
            $scope.sneakersListing = response.data.results;
        });
    }
    ])
    .controller('SneakersDetailsCtrl', ['$scope', '$http', '$stateParams', function($scope, $http, $stateParams) {
        $scope.id = $stateParams.id;

        $http.get('http://localhost:8200/products/' + $scope.id).then(function (response) {
            $scope.sneakers = response.data;
        });
    }
    ]);
