angular
    .module('restShopApp')
    .controller('CartController', CartController);

function CartController($rootScope, cartOrderDataService, userDataService, _) {
    let vm = this;

    vm.cartUnits = [];
    vm.changeQuantity = _.debounce(changeQuantity, 600);
    vm.deleteItem = deleteItem;
    vm.deliveryInfo = {};
    vm.getTotalSum = getTotalSum;
    vm.loading = true;
    vm.onQuantityChange = onQuantityChange;
    vm.placeOrder = placeOrder;
    vm.successfullyOrdered = false;

    ////////////

    activate();

    function activate() {
        cartOrderDataService.getCart().then((cartUnits) => {
            vm.cartUnits = cartUnits;
            vm.loading = false;

            if (vm.cartUnits.length && $rootScope.isLogged()) {
                userDataService.getDeliveryInfo().then((deliveryInfo) => {
                    vm.deliveryInfo = deliveryInfo;
                });
            }
        });
    }

    function changeQuantity(cartUnit) {
        cartOrderDataService.addToCart(cartUnit.unit.sku, cartUnit.quantity).then(() => {
            cartUnit.actualQuantity = cartUnit.quantity;
        }, () => {
            cartUnit.quantity = cartUnit.actualQuantity;
        });
    }

    function deleteItem(cartUnit) {
        cartOrderDataService.deleteFromCart(cartUnit.unit.sku).then((response) => {
            _.remove(vm.cartUnits, {unit: cartUnit.unit});
        });
    }

    function getTotalSum() {
        return vm.cartUnits.map(cu => cu.quantity * cu.unit.price).reduce((a, b) => a + b, 0);
    }

    function onQuantityChange(change, cartUnit) {
        if (!cartUnit.actualQuantity) {
            cartUnit.actualQuantity = cartUnit.quantity;
        }

        cartUnit.quantity += change;
        vm.changeQuantity(cartUnit);
    }

    function placeOrder() {
        cartOrderDataService.createOrder(vm.deliveryInfo.name,
                                         vm.deliveryInfo.address,
                                         vm.deliveryInfo.phone).then((response) => {
            vm.successfullyOrdered = true;
        });
    }
}
