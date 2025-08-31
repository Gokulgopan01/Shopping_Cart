from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Product, Users, Cart

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class AddToCartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

    class Meta:
        model = Cart
        fields = ['user_id', 'product_id', 'quantity']  # Required Meta

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product with given ID does not exist.")
        return value

    def validate_user_id(self, value):
        if not Users.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with given ID does not exist.")
        return value

    def create(self, validated_data):
        user_id = validated_data['user_id']
        product_id = validated_data['product_id']
        quantity = validated_data.get('quantity', 1)

        cart_item, created = Cart.objects.get_or_create(
            user_id=user_id,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item
    
    
class CartStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['order_status']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['user_email', 'user_name', 'password']  # Match model fields

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
