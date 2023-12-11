from rest_framework.serializers import ModelSerializer,Serializer
from .models import *
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

    def to_representation(self, instance) -> dict:
        representation = super().to_representation(instance)
        representation['country'] = instance.country.name
        return representation



class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','manufacturer','category','price','value','unit','manufacturing_date','expired_date', 'image']

    def to_representation(self, instance) -> dict:
        representation = super().to_representation(instance)
        representation['manufacturer'] = instance.manufacturer.name
        representation['category'] = instance.category.name
        return representation

class ProductsCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','manufacturer','category','price','value','unit','manufacturing_date','expired_date', 'image']


class UserSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'phone', 'first_name', 'last_name', 'email', 'is_staff', 'birth_date', 'wallet', 'is_superuser']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone', 'first_name', 'last_name', 'birth_date']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'birth_date']

    def create(self, validated_data):  # Вызывается с помощью методы .save()
        user = Customer.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance) -> dict:
        representation = super().to_representation(instance)
        representation['product'] = instance.product.name
        representation['customer'] = instance.customer.email
        representation['status'] = instance.status
        return representation


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['product','delivery_address',]

    def create(self,validated_data):
        instance = super().create(validated_data)
        instance.customer = self.context.get('request').user
        instance.save()
        return instance



