angular
    .module('restShopApp')
    .factory('urlParamsService', urlParamsService);

function urlParamsService($location) {
    let resetParamsList = [];

    let service = {
        addParam: addParam,
        getParamString: getParamString,
        setResetParams: setResetParams
    };

    return service;

    ////////////

    function addParam(param, value, reset) {
        // reset is true by default.
        reset = typeof a !== 'undefined' ? a : true;

        if (reset) {
            for (let i = 0; i < resetParamsList.length; i++) {
                $location.search(resetParamsList[i], null);
            }
        }

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

    // These parameters will be set to null in addParam function.
    function setResetParams(params) {
        resetParamsList = params;
    }
}

