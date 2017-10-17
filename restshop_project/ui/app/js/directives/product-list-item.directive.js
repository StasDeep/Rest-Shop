angular
    .module('restShopApp')
    .directive('rsProductListItem', productListItem);

function productListItem() {
    let directive = {
        restrict: 'E',
        templateUrl: '/static/partials/product-list-item.html',
        scope: {
            product: '='
        },
        controller: productListItemController,
        controllerAs: 'vm',
        bindToController: true
    };

    return directive;
}

/* @ngInject */
function productListItemController($state, $window) {
    let vm = this;

    vm.applyTag = applyTag;

    ////////////

    function applyTag($event, tagName) {
        $event.preventDefault();
        $event.stopPropagation();
        $window.location.href = $state.href('product-list', {}, {absolute: true}) + '?tags=' + encodeURIComponent(tagName);
    }
}
