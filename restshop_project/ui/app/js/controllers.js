'use strict';
angular.module('myApp.controllers', [])
    .controller('SneakersCtrl', ['$scope', '$stateParams', function($scope, $stateParams) {
        $scope.sneakersListing = [
            {
                "id": 7,
                "title": "Adidas Yeezy Boost",
                "tags": [
                    "Lifestyle"
                ],
                "image": "product_images/empty.jpg"
            },
            {
                "id": 4,
                "title": "LeBron Soldier XI",
                "tags": [
                    "Basketball",
                    "Men"
                ],
                "image": "product_images/lebron-soldier-xi-mens-basketball-shoe.jpg"
            },
            {
                "id": 6,
                "title": "Nike Air Force 1",
                "tags": [
                    "Lifestyle",
                    "Women"
                ],
                "image": "product_images/empty.jpg"
            },
            {
                "id": 1,
                "title": "Nike Air Huarache",
                "tags": [
                    "Lifestyle",
                    "Men"
                ],
                "image": "product_images/air-huarache-mens-shoe.jpg"
            },
            {
                "id": 2,
                "title": "Nike Air Max 97 Premium",
                "tags": [
                    "Lifestyle",
                    "Men"
                ],
                "image": "product_images/air-max-97-premium-mens-shoe.jpg"
            },
            {
                "id": 3,
                "title": "Nike Air VaporMax Flyknit",
                "tags": [
                    "Men",
                    "Running"
                ],
                "image": "product_images/empty.jpg"
            }
        ];
    }
    ])
    .controller('SneakersDetailsCtrl', ['$scope', '$stateParams', function($scope, $stateParams) {
        $scope.id = $stateParams.id;
        $scope.sneakers = {
            "id": 1,
            "title": "Nike Air Huarache",
            "tags": [
                "Lifestyle",
                "Men"
            ],
            "units": [
                {
                    "sku": "151342",
                    "price": 95,
                    "properties": [
                        {
                            "value": "Black",
                            "name": "Color"
                        },
                        {
                            "value": "42",
                            "name": "Size"
                        }
                    ],
                    "images": [
                        "ui/app/product_images/empty.jpg"
                    ],
                    "num_in_stock": 5
                },
                {
                    "sku": "235423",
                    "price": 115,
                    "properties": [
                        {
                            "value": "Red",
                            "name": "Color"
                        },
                        {
                            "value": "44",
                            "name": "Size"
                        }
                    ],
                    "images": [
                        "product_images/air-huarache-mens-shoe_1.jpg",
                        "product_images/air-huarache-mens-shoe.jpg"
                    ],
                    "num_in_stock": 5
                },
                {
                    "sku": "345737",
                    "price": 105,
                    "properties": [
                        {
                            "value": "Red",
                            "name": "Color"
                        },
                        {
                            "value": "42",
                            "name": "Size"
                        }
                    ],
                    "images": [
                        "product_images/air-huarache-mens-shoe_1.jpg",
                        "product_images/air-huarache-mens-shoe.jpg"
                    ],
                    "num_in_stock": 5
                },
                {
                    "sku": "626823",
                    "price": 95,
                    "properties": [
                        {
                            "value": "Metallic Silver",
                            "name": "Color"
                        },
                        {
                            "value": "40",
                            "name": "Size"
                        }
                    ],
                    "images": [
                        "ui/app/product_images/empty.jpg"
                    ],
                    "num_in_stock": 5
                }
            ]
        }
    }
    ]);
