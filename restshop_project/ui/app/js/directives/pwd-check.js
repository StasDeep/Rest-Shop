angular
    .module('restShopApp')
    .directive('pwdCheck', pwdCheck);

function pwdCheck() {
    let directive = {
        require: 'ngModel',
        scope: {
            password: '=pwdCheck'
        },
        link: (scope, elem, attrs, ngModel) => {
            scope.$watch('password', () => ngModel.$validate());

            ngModel.$validators.pwMatch = (passwordConfirmation) => {
                console.log(passwordConfirmation, scope.password, passwordConfirmation == scope.password);
                return passwordConfirmation == scope.password;
            }
        }
    };

    return directive;
}
