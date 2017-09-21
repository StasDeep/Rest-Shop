angular
    .module('restShopApp')
    .factory('urlParamsService', urlParamsService);

function urlParamsService($location) {
    let service = {
        addParam: addParam,
        getParamString: getParamString
    };

    return service;

    ////////////

    function addParam(param, value) {
        $location.search(param, value);
    }

    // listParams stores names of parameters which are represented as comma separated lists.
    function getParamString(listParams) {
        let paramString = '?';

        let params = $location.search();

        for (let name in params) {
            if (!params.hasOwnProperty(name)) {
                // Current property is not a direct property of params.
                continue;
            }

            let value = params[name];

            if (listParams.includes(name)) {
                // If param is in listParams, then it's likely to be comma separated.
                let values = value.split(',');

                for (let i = 0; i < values.length; i++) {
                    paramString += name + '=' + values[i] + ';';
                }
            } else {
                paramString += name + '=' + value + ';';
            }
        }

        return paramString;
    }
}

