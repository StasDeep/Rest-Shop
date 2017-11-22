angular
    .module('restShopApp')
    .controller('CartController', CartController);

function CartController(cartOrderDataService, _) {
    let vm = this;

    vm.cartUnits = [];
    vm.changeQuantity = _.debounce(changeQuantity, 600);
    vm.deleteItem = deleteItem;
    vm.loading = true;
    vm.onQuantityChange = onQuantityChange;

    ////////////

    activate();

    function activate() {
        cartOrderDataService.getCart().then((cartUnits) => {
            vm.cartUnits = cartUnits;
            vm.loading = false;
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

    function onQuantityChange(change, cartUnit) {
        if (!cartUnit.actualQuantity) {
            cartUnit.actualQuantity = cartUnit.quantity;
        }

        cartUnit.quantity += change;
        vm.changeQuantity(cartUnit);
    }
}
