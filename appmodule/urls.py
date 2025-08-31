from django.conf import settings
from django.urls import path
from .views import ProductCreateView, ProductAllView, ProductDetailView, ProductDelete, LoginView, RegisterView, CartView, CartStatusUpdateView
from django.conf.urls.static import static

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/create-prouct/', ProductCreateView.as_view(), name='product-create'),
    path('api/view-products/', ProductAllView.as_view(), name='product-list'),
    path('api/detailed-view/<int:id>/',ProductDetailView.as_view(), name='product-detail'),
    path('api/delete-product/<int:id>/',ProductDelete.as_view(), name='product-delete'),

    path('api/cart/', CartView.as_view(), name='cart-list-create'),
    path('api/cart/<int:pk>/', CartView.as_view(), name='cart-detail'),
    path('cart/<int:pk>/status/', CartStatusUpdateView.as_view(), name='cart-status-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
