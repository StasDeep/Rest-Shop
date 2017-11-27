angular
    .module('restShopApp')
    .factory('userDataService', userDataService);

function userDataService($http, $rootScope, config) {
    let service = {
        getDeliveryInfo: getDeliveryInfo,
        getUser: getUser,
        login: login,
        logout: logout,
        setDeliveryInfo: setDeliveryInfo,
        setPassword: setPassword,
        setUser: setUser,
        signup: signup
    };

    return service;

    ////////////

    function getDeliveryInfo() {
        return $http.get(config.apiUrl + '/deliveryinfo/').then((response) => {
            return response.data.data;
        });
    }

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

    function setDeliveryInfo(deliveryInfo) {
        return $http.post(config.apiUrl + '/deliveryinfo/', deliveryInfo);
    }

    function setPassword(password) {
        return $http.post(config.apiUrl + '/password/', {password: password});
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
