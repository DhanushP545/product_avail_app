from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.buyer_home, name='buyer_home'),
    path('pre-bookings/', views.view_pre_bookings, name='view_pre_bookings'),
    path('pre-bookings/<int:booking_id>/accept/', views.accept_prebooking, name='accept_prebooking'),
    path('pre-bookings/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('pre-bookings/confirm/<int:booking_id>/', views.confirm_prebooking, name='confirm_prebooking'),
    path('pre-bookings/cancel/<int:booking_id>/', views.cancel_prebooking, name='cancel_prebooking'),

    path('', views.buyer_home, name='buyer_home'),
    path('search/', views.buyer_home, name='search_products'),
    path('category/<int:category_id>/', views.view_category_products, name='view_category_products'),
    path('shop/<int:shop_id>/', views.view_shop_products, name='view_shop_products'),
    path('prebook/<int:product_id>/', views.prebook_product, name='prebook_product'),

]
