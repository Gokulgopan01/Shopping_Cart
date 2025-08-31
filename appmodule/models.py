from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.conf import settings


#product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    size = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    product_info =models.TextField(blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

#Cart models
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length =50, 
    choices=[("Carted", "Carted"),
            ("Ordered", "Ordered"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),], default="pending")

    class Meta:
        unique_together = ('user', 'product') 

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    

#Auth models
class UserManager(BaseUserManager): 
    def create_user(self, user_email, password=None, **extra_fields):
        if not user_email:
            raise ValueError("Email is required")
        user_email = self.normalize_email(user_email)
        user = self.model(user_email=user_email, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    user_email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150)
    user_phone = models.CharField(max_length=15, blank=True, null=True)
    user_address = models.TextField(blank=True, null=True)
    user_zipcode = models.CharField(max_length=10, blank=True, null=True)
    user_city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_email' 
    REQUIRED_FIELDS = ['user_name']  

    objects = UserManager()

    def __str__(self):
        return self.user_email
    


