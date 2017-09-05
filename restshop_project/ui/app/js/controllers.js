'use strict';
angular.module('myApp.controllers', [])
    .controller('SneakersCtrl', ['$scope', '$http', '$location', 'config', function($scope, $http, $location, config) {
        $scope.go = function (path) {
            $location.path(path);
        };

        $http.get(config.serverUrl + '/products/').then(function (response) {
            var items = response.data.results;
            for (var i = 0; i < items.length; i++) {
                if (items[i].image === null) {
                    items[i].image = config.emptyImageUrl;
                } else {
                    items[i].image = config.serverUrl + items[i].image;
                }
            }
            $scope.sneakersListing = items;
        });
    }
    ])
    .controller('SneakersDetailsCtrl', ['$scope', '$http', '$stateParams', function($scope, $http, $stateParams) {
        $scope.id = $stateParams.id;

        $http.get(config.serverUrl + '/products/' + $scope.id).then(function (response) {
            $scope.sneakers = response.data;
        });
    }
    ]);
