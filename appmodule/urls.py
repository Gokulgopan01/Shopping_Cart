from django.conf import settings
from django.urls import path
from .views import ProductCreateView, ProductAllView, ProductDetailView, ProductDelete, LoginView, RegisterView, AddToCartView, CartStatusUpdateView, UserCartView, UserProfileView
from django.conf.urls.static import static

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),                    #Register api
    path('api/auth/login/', LoginView.as_view(), name='login'),                             #Login api
    path('api/user/profile/<int:id>/',UserProfileView.as_view(), name='user-profile'),      #User profile view api
    path('api/view-products/', ProductAllView.as_view(), name='product-list'),              #Product list api
    path('api/detailed-view/<int:id>/',ProductDetailView.as_view(), name='product-detail'), #Product detail api
    path('api/cart/add/', AddToCartView.as_view(), name='add-to-cart'),                     #Add to cart api
    path('api/cart/', UserCartView.as_view(), name='user-cart'),                            #User cart view api

    #Admin roles     
    path('api/delete-product/<int:id>/',ProductDelete.as_view(), name='product-delete'),                          
    path('api/create-prouct/', ProductCreateView.as_view(), name='product-create'), 
    path('cart/<int:pk>/status/', CartStatusUpdateView.as_view(), name='cart-status-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
