from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('create-shop/', views.create_shop, name='create_shop'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
