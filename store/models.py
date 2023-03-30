from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Category(models.Model):
    name                    = models.CharField(max_length=300)
    description             = models.TextField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    username                = models.CharField(max_length=50, unique=True)
    first_name              = models.CharField(max_length=50)
    last_name               = models.CharField(max_length=50)
    email                   = models.EmailField(max_length=254)
    shipping_address_1      = models.CharField(max_length=100)
    shipping_address_2      = models.CharField(max_length=100, blank=True)
    shipping_city           = models.CharField(max_length=50)
    shipping_state          = models.CharField(max_length=50)
    shipping_zip_code       = models.CharField(max_length=10)
    shipping_country        = models.CharField(max_length=50)
    password_hash           = models.CharField(max_length=250)
    
    def set_password(self, password):
        self.password_hash = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password_hash)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#products section 
class Product(models.Model): 
    name                    = models.CharField(max_length=300)
    description             = models.TextField()
    price                   = models.DecimalField(max_digits=9,decimal_places=2)
    image                   = models.ImageField(upload_to='Products/')
    category                = models.ForeignKey(Category, on_delete= models.CASCADE)
    specifications          = models.TextField()
    quantity                = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer                = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date              = models.DateTimeField(auto_now_add=True)
    shipping_address        = models.CharField(max_length=255)
    order_total             = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method          = models.CharField(max_length=50)
    payment_data            = models.TextField()
    fulfilled               = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order #{self.id} for {self.customer}"


    
class Revenue(models.Model):
    date                    = models.DateField()
    total_revenue           = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Revenue Data#{self.date}"
