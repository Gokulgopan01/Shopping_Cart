from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer, LoginSerializer, RegisterSerializer, CartSerializer, AddToCartSerializer, CartStatusSerializer
from .models import Product, Cart

#Product Views

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductAllView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


#Authentication Views

class RegisterView(APIView):
    '''View to handle Registration'''

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    '''View to handle Login'''

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['user_email']
            password = serializer.validated_data['password']
            user = authenticate(request, user_email=user_email, password=password) 
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh),'access': str(refresh.access_token),})
            return Response({'detail': 'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

#Cart crete and get
 
class CartView(APIView):
    ''' View to handle cart operation'''

    permission_classes =[IsAuthenticated]

    #Get Cart items
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).select_related('product')
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Add to Cart
    def post(self, request):
        serializer = AddToCartSerializer(data= request.data)
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #Update cart view (quantity , size. colour)
    def put(self, request, pk):
        cart_items = Cart.get_object_or_404(Cart, pk=pk, user=request.user)
        serializer = CartSerializer(cart_items, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #dlete cart item
    def delete(self, request, pk):
        """Delete a specific product from cart"""
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
    

#Update Cart status
class CartStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            cart_item = Cart.objects.get(pk=pk, user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartStatusSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated", "cart": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







    



