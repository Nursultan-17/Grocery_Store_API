from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomerManager


UNIT_CHOICES = [
    ('kg', 'Kilogramms'),
    ('g', 'Gramms'),
    ('m', 'Meters'),
    ('cm', 'Centimeters'),
    ('mm', 'Millimeters'),
    ('piece', 'Piece'),
    ('pack', 'Pack'),
    ('box', 'Box'),
    ('l', 'Liter'),
    ('ml', 'Milliliter'),
]


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    wallet = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products')
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    manufacturing_date = models.DateField()
    expired_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    STATUS_CHOISES = (
        ('delivery','delivery'),
        ("not delivery","not delivery")

    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer',null=True,blank=True, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=100)
    phone_customer = models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(max_length=20,default='not delevery',choices=STATUS_CHOISES)

    def save(self, *args, **kwargs):
        if self.status == 'delivery':
            self.customer.wallet +=500
        if self.customer:
            self.phone_customer = self.customer.phone
        # if self.customer.wallet > 0:
        super().save(*args, **kwargs)






