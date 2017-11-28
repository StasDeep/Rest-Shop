angular
    .module('restShopApp')
    .factory('userDataService', userDataService);

function userDataService(apiService, $rootScope) {
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
        return apiService.get('deliveryinfo').then((response) => {
            return response.data.data;
        });
    }

    function getUser() {
        return apiService.get('user').then((response) => {
            return response.data.data;
        });
    }

    function login(username, password) {
        return apiService.post('auth', {
            username: username,
            password: password
        }).then((response) => {
            return setUser();
        });
    }

    function logout() {
        return apiService.delete('auth').then((response) => {
            $rootScope.user = null;
        });
    }

    function setDeliveryInfo(deliveryInfo) {
        return apiService.post('deliveryinfo', deliveryInfo);
    }

    function setPassword(password) {
        return apiService.post('password', {password: password});
    }

    function setUser() {
        return getUser().then((user) => {
            $rootScope.user = user;
            return user;
        });
    }

    function signup(email, password) {
        return apiService.post('user/create', {
            email: email,
            password: password
        });
    }
}
