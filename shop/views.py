from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser


from .models import *
from .serializers import *

from django.contrib.auth import login, logout, authenticate

class CategoryApiView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: CategorySerializer()
        }
    )
    def get(self, request):
        categories = Category.objects.all()
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            categories = categories.order_by(ordering)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            categories = categories.filter(name__contains=search)
        data = CategorySerializer(categories, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: CategorySerializer(),
            403: 'Only admin can add categories',
            400: 'Bad request'
        }
    )
    def post(self, request):
        if request.user.is_staff:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only admin can add categories'}, status=HTTP_403_FORBIDDEN)

class CategoryDetailApiView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(responses={200: CategorySerializer()})
    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        data = CategorySerializer(category).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CategorySerializer(),
        responses={
            200: CategorySerializer(),
            400: 'Bad request',
            403: 'Only admin can change categories'
        }
    )
    def patch(self, request, pk):
        if request.user.is_staff:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only admin can change categories'}, status=HTTP_403_FORBIDDEN)

    @swagger_auto_schema(responses={200: 'Object is deleted!', 403: 'Only admin can delete categories'})
    def delete(self, request, pk):
        if request.user.is_staff:
            category = Category.objects.get(id=pk)
            category.delete()
            return Response({'message': 'Object is deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Only admin can delete categories'}, status=HTTP_403_FORBIDDEN)


class ManufacturerApiView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: ManufacturerSerializer()
        }
    )
    def get(self, request):
        manufacturer = Manufacturer.objects.all()
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            manufacturer = manufacturer.order_by(ordering)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            manufacturer = manufacturer.filter(name__contains=search)
        data = ManufacturerSerializer(manufacturer, many=True).data
        return Response(data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name','country','address','email'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'country': openapi.Schema(type=openapi.TYPE_INTEGER),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: ManufacturerSerializer(),
            400: 'Bad request',
            403: 'Only admin can add a manufacturer',
        }
    )
    def post(self, request):
        if request.user.is_staff:
            serializer = ManufacturerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only admin can add a manufacturer'}, status=HTTP_403_FORBIDDEN)


class ManufacturerDetailApiView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(responses={200: ManufacturerSerializer()})
    def get(self, request, pk):
        manufacturer = Manufacturer.objects.get(id=pk)
        data = ManufacturerSerializer(manufacturer).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ManufacturerSerializer(),
        responses={
            200: CategorySerializer(),
            400: 'Bad request',
            403: 'Only the admin can change the manufacturer'
        }
    )
    def patch(self, request, pk):
        if request.user.is_staff:
            manufacturer = Manufacturer.objects.get(id=pk)
            serializer = ManufacturerSerializer(manufacturer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only the admin can change the manufacturer'}, status=HTTP_403_FORBIDDEN)

    @swagger_auto_schema(responses={200: 'Object is deleted!', 403: 'Only admin can delete a manufacturer'})
    def delete(self, request, pk):
        if request.user.is_staff:
            manufacturer = Manufacturer.objects.get(id=pk)
            manufacturer.delete()
            return Response({'message': 'Object is deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Only admin can delete a manufacturer'}, status=HTTP_403_FORBIDDEN)


class CountryApiView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: CountrySerializer()
        }
    )
    def get(self, request):
        country = Country.objects.all()
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            country = country.order_by(ordering)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            country = country.filter(name__contains=search)
        data = CountrySerializer(country, many=True).data
        return Response(data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),

            }
        ),
        responses={
            200: CountrySerializer(),
            400: 'Bad request',
            403: 'Only the administrator can add country',
        }
    )
    def post(self, request):
        if request.user.is_staff:
            serializer = CountrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only the administrator can add country'}, status=HTTP_403_FORBIDDEN)


class CountryDetailApiView(APIView):
    permission_classes = [permissions.AllowAny, ]

    @swagger_auto_schema(responses={200: CountrySerializer()})
    def get(self, request, pk):
        country = Country.objects.get(id=pk)
        data = CountrySerializer(country).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CountrySerializer(),
        responses={
            200: CategorySerializer(),
            400: 'Bad request',
            403: 'Only the admin can change the country'
        }
    )
    def patch(self, request, pk):
        if request.user.is_staff:
            country = Country.objects.get(id=pk)
            serializer = CountrySerializer(country, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only the admin can change the country'}, status=HTTP_403_FORBIDDEN)

    @swagger_auto_schema(responses={200: 'Object is deleted!', 403: 'Only admin can delete a country'})
    def delete(self, request, pk):
        if request.user.is_staff:
            country = Country.objects.get(id=pk)
            country.delete()
            return Response({'message': 'Object is deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Only admin can delete a country'}, status=HTTP_403_FORBIDDEN)


class ProductsApiView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: ProductsSerializer()
        }
    )
    def get(self, request):
        products = Product.objects.all()
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            products = products.order_by(ordering)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            products = products.filter(name__contains=search).union(products.filter(description__contains=search))
        data = ProductsSerializer(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='name',in_=openapi.IN_FORM,type=openapi.TYPE_STRING,required=True),
            openapi.Parameter(name='description', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(name='manufacturer', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter(name='category', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter(name='price', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter(name='value', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter(name='unit', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter(name='manufacturing_date', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter(name='expired_date', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter(name='image', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
        ],
        responses={
            200: ProductsSerializer(),
            400: 'Bad request',
            403: 'Only admin can add products'
        }
    )
    def post(self, request):
        if request.user.is_staff:
            serializer = ProductsCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only admin can add products'}, status=HTTP_403_FORBIDDEN)


class ProductsDetailApiView(APIView):
    permission_classes = [permissions.AllowAny, ]
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(responses={200: ProductsSerializer()})
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        data = ProductsSerializer(product).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='name',in_=openapi.IN_FORM,type=openapi.TYPE_STRING),
            openapi.Parameter(name='description', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(name='manufacturer', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='category', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='price', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='value', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='unit', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(name='manufacturing_date', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(name='expired_date', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(name='image', in_=openapi.IN_FORM, type=openapi.TYPE_FILE),
        ],
        responses={
            200: ProductsSerializer(),
            400: 'Bad request',
            403: 'Only admin can change products'
        }
    )
    def patch(self, request, pk):
        if request.user.is_staff:
            product = Product.objects.get(id=pk)
            serializer = ProductsSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only the admin can change the product'}, status=HTTP_403_FORBIDDEN)

    @swagger_auto_schema(responses={200: 'Object is deleted!', 403: 'Only admin can delete a product'})
    def delete(self, request, pk):
        if request.user.is_staff:
            product = Product.objects.get(id=pk)
            product.delete()
            return Response({'message': 'Object is deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Only admin can delete a product'}, status=HTTP_403_FORBIDDEN)


class AuthApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'Welcome!',
            403: 'Username or/and Password is not valid!',
        }
    )
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = {'message': 'Welcome!'}
            return Response(data, HTTP_200_OK)
        else:
            data = {'message': 'Username or/and Password is not valid!'}
            return Response(data, HTTP_403_FORBIDDEN)


class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data, status=HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer(),
        responses={
            200: UserSerializer(),
            400: 'Bad request',
        }
    )
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = UserSerializer(user).data
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'User is deleted!'})
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'User is deleted!'}, status=HTTP_200_OK)


class RegistrationApiView(APIView):
    permission_classes = [AllowAny, ]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'first_name', 'last_name', 'phone', 'birth_date'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'birth_date': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'User successfully registered',
            400: 'Bad request',
        }
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logout(request)
        return Response({'message': 'You logged out successfully'}, status=HTTP_200_OK)




class OrderApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: CategorySerializer()
        }
    )
    def get(self,request):
        user = request.user
        order = Order.objects.filter(customer=user)
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            order = order.order_by(ordering)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            order = order.filter(name__contains=search)
        data = OrderSerializer(order, many=True).data
        return Response(data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='product',in_=openapi.IN_FORM,type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='delivery_address', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
        responses={
            200: OrderSerializer(),
            400: 'Bad request',
        }
    )
    def post(self, request):
        product = Product.objects.get(id=request.data['product'])
        user = Customer.objects.get(email=request.user)
        total = 0
        if user.wallet > product.price:
            user.wallet -= product.price
            user.save()
            total = 0
        if user.wallet < product.price:
            product.price -= user.wallet
            total = product.price
            user.wallet = 0
            user.save()
        if user.wallet == product.price:
            user.wallet = 0
            user.save()
            total = 0
        serializer = OrderCreateSerializer(data=request.data,context={'request': request,'final_price': total})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailApiView(APIView):
    permission_classes = [permissions.AllowAny, ]
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(responses={200: OrderSerializer()})
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        data = OrderSerializer(order).data
        return Response(data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='customer', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='delivery_address', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(name='status', in_=openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
        responses={
            200: OrderSerializer(),
            400: 'Bad request',
            403: 'Only admin can change order'
        }
    )
    def patch(self, request, pk):
        if request.user.is_staff:
            order = Order.objects.get(id=pk)
            serializer = OrderPatchSerializer(order, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                if request.data["status"] == "delivery":
                    customer_wallet = Customer.objects.get(email=request.user)
                    customer_wallet.wallet += 500
                    customer_wallet.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only the admin can change the order'}, status=HTTP_403_FORBIDDEN)


    @swagger_auto_schema(responses={200: 'Object is deleted!', 403: 'Only admin can delete a order'})
    def delete(self, request, pk):
        if request.user.is_staff:
            order = Order.objects.get(id=pk)
            order.delete()
            return Response({'message': 'Object is deleted!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Only admin can delete a order'}, status=HTTP_403_FORBIDDEN)





