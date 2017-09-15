angular
    .module('restShopApp')
    .factory('urlParamsService', urlParamsService);

function urlParamsService($location) {
    var resetParamsList = [];

    var service = {
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
            for (var i = 0; i < resetParamsList.length; i++) {
                $location.search(resetParamsList[i], null);
            }
        }

        $location.search(param, value);
    }

    // listParams stores names of parameters which are represented as comma separated lists.
    function getParamString(listParams) {
        var paramString = '?';

        var params = $location.search();

        for (var name in params) {
            if (!params.hasOwnProperty(name)) {
                // Current property is not a direct property of params.
                continue;
            }

            var value = params[name];

            if (listParams.includes(name)) {
                // If param is in listParams, then it's likely to be comma separated.
                var values = value.split(',');

                for (var i = 0; i < values.length; i++) {
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

