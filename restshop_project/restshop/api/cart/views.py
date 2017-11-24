from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from restshop.api.cart.models import CartUnit
from restshop.api.cart.serializers import CartUnitSerializer
from restshop.api.unit.models import Unit


class CartView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()

        return Response(CartUnitSerializer(cart_units.order_by('unit__sku'), many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartUnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        unit = Unit.objects.get(sku=data['sku'])

        cart_unit_data = {
            'unit': unit,
            'user': None,
            'session': None
        }

        if not bool(request.user.is_anonymous):
            cart_unit_data['user'] = request.user
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_unit_data['session'] = Session.objects.get(session_key=request.session.session_key)

        cart_unit = CartUnit.objects.filter(**cart_unit_data).first()

        if cart_unit is None:
            cart_unit = CartUnit(**cart_unit_data)

        cart_unit.quantity = data['quantity']
        cart_unit.save()

        return Response(status=status.HTTP_201_CREATED)


class CartUnitView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, sku=None):
        if not bool(request.user.is_anonymous):
            cart_units = request.user.cart_units.all()
        else:
            if request.session.session_key is None:
                request.session.save()

            cart_units = Session.objects.get(session_key=request.session.session_key).cart_units.all()

        cart_unit = cart_units.filter(unit__sku=sku).first()

        if cart_unit is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_unit.delete()

        return Response(status=status.HTTP_200_OK)
