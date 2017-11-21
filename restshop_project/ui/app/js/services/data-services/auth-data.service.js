angular
    .module('restShopApp')
    .factory('authDataService', authDataService);

function authDataService($http, $rootScope, config) {
    let service = {
        getUser: getUser,
        login: login,
        logout: logout,
        setUser: setUser,
        signup: signup
    };

    return service;

    ////////////

    function getUser() {
        return $http.get(config.apiUrl + '/user/').then((response) => {
            return response.data.data;
        });
    }

    function login(username, password) {
        return $http.post(config.apiUrl + '/auth/', {
            username: username,
            password: password
        }).then((response) => {
            return setUser();
        });
    }

    function logout() {
        return $http.delete(config.apiUrl + '/auth/').then((response) => {
            $rootScope.user = null;
        });
    }

    function setUser() {
        return getUser().then((user) => {
            $rootScope.user = user;
            return user;
        });
    }

    function signup(email, password) {
        return $http.post(config.apiUrl + '/user/create/', {
            email: email,
            password: password
        });
    }
}
