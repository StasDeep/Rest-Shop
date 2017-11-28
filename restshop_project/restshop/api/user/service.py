from restshop.api.user.models import DeliveryInfo


class DeliveryInfoService:

    @staticmethod
    def delete_by_user(user):
        """Remove current delivery info for user, if exists.
        Return True if successfully deleted.
        """
        try:
            user.deliveryinfo.delete()
            return True
        except DeliveryInfo.DoesNotExist:
            return False
