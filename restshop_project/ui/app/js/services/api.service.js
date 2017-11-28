angular
    .module('restShopApp')
    .factory('apiService', apiService);

function apiService($http, config) {
    let service = {
        delete: delete_,
        get: get,
        post: post
    };

    return service;

    ////////////

    function delete_(url, id) {
        return $http.delete(getFullUrl(url, id));
    }

    function get(url, id, paramString) {
        return $http.get(getFullUrl(url, id, paramString));
    }

    function getFullUrl(url, id, paramString) {
        return config.apiUrl + '/' + url + '/' + (!!id ? id + '/' : '') + (!!paramString ? '?' + paramString : '');
    }

    function post(url, data, id) {
        return $http.post(getFullUrl(url, id), data);
    }
}
