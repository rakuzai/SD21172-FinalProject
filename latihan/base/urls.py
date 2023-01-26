from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name='home'),
    path('list-menu/', views.listMenu, name='list-menu'),
    path('create-order/', views.create_order, name='create-order'),
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('make_payment/<int:pk>/', views.make_payment, name='make_payment'),
    path('payment_receipt/<int:pk>/', views.payment_receipt, name='payment_receipt'),
    path('tampil-grafik/', views.tampilGrafik, name='tampil-grafik')
]