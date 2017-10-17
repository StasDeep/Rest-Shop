angular
    .module('restShopApp')
    .factory('orderingService', orderingService);

/* @ngInject */
function orderingService(_) {
    let service = {
        orderProperties: orderProperties,
        orderTags: orderTags
    };

    return service;

    ////////////

    function orderProperties(properties, valuesKey) {
        valuesKey = valuesKey || 'values';

        for (let prop of properties) {
            if (prop.name.toLowerCase() == 'size') {
                prop[valuesKey] = orderSizes(prop[valuesKey]);
            }
        }

        return properties;
    }

    function orderSizes(sizes) {
        return _.sortBy(sizes, [
            x => parseFloat(x.value) || Number.MAX_VALUE,
            x => parseFloat(x.value.split(' ')[1])
        ]);
    }

    function orderTags(tags) {
        return _.sortBy(tags, [
           x => x.toLowerCase() != 'men',
           x => x.toLowerCase() != 'women',
           x => x
        ]);
    }
}
