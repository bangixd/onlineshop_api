from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Order
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).last()
        if not cart or not cart.items.exists():
            return Response({"detail": "سبد خرید شما خالی است."}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی موجودی محصولات
        for item in cart.items.all():
            if item.quantity > item.product.inventory:
                return Response(
                    {"detail": f"موجودی محصول '{item.product.name}' کافی نیست."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = serializer.save(user=self.request.user)
        order.calculate_total_price()

        # کاهش موجودی محصولات و خالی کردن سبد خرید
        for item in cart.items.all():
            item.product.inventory -= item.quantity
            item.product.save()

        cart.items.all().delete()  # خالی کردن سبد خرید