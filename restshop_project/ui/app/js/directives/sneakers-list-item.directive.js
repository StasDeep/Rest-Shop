angular
    .module('restShopApp')
    .directive('rsSneakersListItem', sneakersListItem);

function sneakersListItem($state, $window) {
    let directive = {
        restrict: 'E',
        templateUrl: '/static/partials/sneakers-list-item.html',
        scope: {
            sneakers: '='
        },
        controller: sneakersListItemController,
        controllerAs: 'vm',
        bindToController: true
    };

    return directive;
}

/* @ngInject */
function sneakersListItemController($state, $window) {
    let vm = this;

    vm.applyTag = applyTag;

    ////////////

    function applyTag($event, tagName) {
        $event.stopPropagation();
        $window.location.href = $state.href('sneakers', {}, {absolute: true}) + '?tags=' + tagName;
    }
}
