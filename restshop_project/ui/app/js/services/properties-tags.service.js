angular
    .module('restShopApp')
    .factory('propertiesTagService', propertiesTagService);

function propertiesTagService(_) {
    let service = {
        filterProperties: filterProperties,
        orderProperties: orderProperties,
        orderTags: orderTags
    };

    return service;

    ////////////

    function createMapping(values) {
        let mapping = {};

        for (let value of values) {
            mapping[value.value] = [value.id];
        }

        return [values.map(v => v.value), mapping];
    }

    function filterColors(colors) {
        let uniqueColors = [
            'Black',
            'Grey',
            'White',
            'Red',
            'Blue',
            'Green',
            'Yellow',
            'Pink',
            'Orange'
        ].sort();

        let mapping = {};

        for (let uniqueColor of uniqueColors) {
            mapping[uniqueColor] = [];
            for (let color of colors) {
                if (color.value.toLowerCase().includes(uniqueColor.toLowerCase())) {
                    mapping[uniqueColor].push(color.id);
                }
            }
        }

        return [uniqueColors, mapping];
    }

    function filterProperties(properties) {
        for (let prop of properties) {
            let result = [];

            if (prop.name.toLowerCase() == 'size') {
                result = filterSizes(prop['values']);
            } else if (prop.name.toLowerCase() == 'color') {
                result = filterColors(prop['values']);
            } else {
                result = createMapping(prop['values']);
            }

            prop['values'] = result[0].map(v => { return {value: v} });
            prop['mapping'] = result[1];

            if (prop.name.toLowerCase() == 'size') {
                prop['values'] = _.sortBy(prop['values'], x => parseFloat(x.value) || Number.MAX_VALUE);
            }
        }

        return properties;
    }

    function filterSizes(sizes) {
        let uniqueSizes = [];

        function addSize(value) {
            if (uniqueSizes.indexOf(value) == -1 && !!value) {
                uniqueSizes.push(value);
            }
        }

        for (let size of sizes) {
            // '9.5' --> ['9.5']
            // 'M 9.5 / W 11.5' --> ['M', '9.5', '/', 'W', '11.5']
            let splittedSize = size.value.split(' ');

            if (splittedSize.length == 1) {
                addSize(splittedSize[0]);
            } else {
                addSize(splittedSize[1]);
                addSize(splittedSize[4]);
            }
        }

        let mapping = {};

        for (let uniqueSize of uniqueSizes) {
            mapping[uniqueSize] = [];
            for (let size of sizes) {
                if (size.value.split(' ').includes(uniqueSize)) {
                    mapping[uniqueSize].push(size.id);
                }
            }
        }

        return [uniqueSizes, mapping];
    }

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
