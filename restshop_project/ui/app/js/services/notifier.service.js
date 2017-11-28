angular
    .module('restShopApp')
    .factory('notifier', notifier);

function notifier(notify) {
    let service = {
        error: error,
        success: success,
        warning: warning
    };

    return service;

    ////////////

    function error(message) {
        notify({
            message: message,
            classes: 'error',
            duration: 6000,
            position: 'right'
        });
    }

    function success(message) {
        notify({
            message: message,
            classes: 'success',
            duration: 4000,
            position: 'right'
        });
    }

    function warning(message) {
        notify({
            message: message,
            classes: 'warning',
            duration: 6500,
            position: 'right'
        });
    }
}
