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
        link: link
    };

    return directive;

    ////////////

    function link(scope, elem, attrs) {
         scope.applyTag = applyTag;

         function applyTag($event, tagName) {
             $event.stopPropagation();
             $window.location.href = $state.href('sneakers', {}, {absolute: true}) + '?tags=' + tagName;
         }
    }
}
