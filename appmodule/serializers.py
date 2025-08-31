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
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

    def Validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product with given ID does not exist.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data['product_id']
        quantity = validated_data.get('quantity', 1)

        cart_item, created = Cart.objects.get_or_create(user=user, product_id=product_id, defaults={'quantity': quantity})
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
