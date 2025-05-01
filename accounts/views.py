from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm, ShopForm
from .models import UserProfile, Shop
from booking.models import PreBooking
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Set role
            role = form.cleaned_data['role']
            UserProfile.objects.filter(user=user).update(role=role)
            if role == 'seller':
                return redirect('create_shop')
            else:
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
@login_required
def create_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                shop.latitude = latitude
                shop.longitude = longitude

            shop.save()
            messages.success(request, 'Shop created successfully!')
            return redirect('seller_dashboard')  # or any page for the seller
    else:
        form = ShopForm()
    return render(request, 'accounts/create_shop.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                role = user.userprofile.role
                if role == 'buyer':
                    return redirect('buyer_home')
                elif role == 'seller':
                    return redirect('seller_dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')
def home(request):
    return render(request, 'booking/buyer_home.html')

@login_required
def user_profile(request):
    pre_bookings = PreBooking.objects.filter(buyer=request.user)

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'pre_bookings': pre_bookings
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        become_seller = request.POST.get('become_seller')
        new_email = request.POST.get('email')
        new_shopname = request.POST.get('shop_name')

        user = request.user
        shop = Shop.objects.get(owner=user)
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_shopname:
            shop.name = new_shopname
        
        if become_seller:
            user.is_seller = True
            user.is_buyer = False  # Optional: You can disable buyer role if needed
        shop.save()
        user.save()
        return redirect('user_profile')

    return redirect('user_profile')

