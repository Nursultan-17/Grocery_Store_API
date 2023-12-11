from django.urls import path
from .views import *

urlpatterns = [
    path('category', CategoryApiView.as_view()),
    path('category/<int:pk>', CategoryDetailApiView.as_view()),

    path('products', ProductsApiView.as_view()),
    path('products/<int:pk>', ProductsDetailApiView.as_view()),

    path('manufacturer', ManufacturerApiView.as_view()),
    path('manufacturer/<int:pk>', ManufacturerDetailApiView.as_view()),

    path('сountry', CountryApiView.as_view()),
    path('сountry/<int:pk>', CountryDetailApiView.as_view()),

    path('orders', OrderApiView.as_view()),
    path('orders/<int:pk>', OrderDetailApiView.as_view()),






    path('sign_in', AuthApiView.as_view()),
    path('sign_out', LogOutApiView.as_view()),
    path('profile', ProfileApiView.as_view()),
    path('sign_up', RegistrationApiView.as_view()),

]