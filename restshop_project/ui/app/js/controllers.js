'use strict';
angular.module('myApp.controllers', [])
    .controller('SneakersCtrl', ['$scope', '$http', '$location', '$anchorScroll', 'config',
        function ($scope, $http, $location, $anchorScroll, config) {
            $scope.go = function (path) {
                $location.path(path);
            };

            $scope.changeList = function (apiPath) {
                $http.get(apiPath).then(function (response) {
                    var items = response.data.results;

                    for (var i = 0; i < items.length; i++) {
                        if (items[i].image === null) {
                            items[i].image = config.emptyImageUrl;
                        } else {
                            items[i].image = config.serverUrl + items[i].image;
                        }
                    }

                    $scope.sneakersListing = items;
                    $scope.prevPageUrl = response.data.previous;
                    $scope.nextPageUrl = response.data.next;

                    // Scroll to top of the page to show new results.
                    $anchorScroll();
                });
            };

            $scope.changeList(config.serverUrl + '/products/');
        }
    ])
    .controller('SneakersDetailsCtrl', ['$scope', '$http', '$stateParams', 'config',
        function ($scope, $http, $stateParams, config) {
            $scope.id = $stateParams.id;

            $http.get(config.serverUrl + '/products/' + $scope.id).then(function (response) {
                $scope.sneakers = response.data;
            });
        }
    ]);
