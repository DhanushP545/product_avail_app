# product_avail_app/context_processors.py

from accounts.models import UserProfile
from shop.models import Shop  # Import UserProfile and Shop from accounts app

def navbar_context(request):
    context = {}
    
    if request.user.is_authenticated:
        # Fetch the UserProfile for the logged-in user
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Set the user role and whether they are a buyer or seller
        context['is_buyer'] = user_profile.role == 'buyer'
        context['is_seller'] = user_profile.role == 'seller'
        
        # Check if the seller has a shop
        if context['is_seller']:
            context['shop_exists'] = Shop.objects.filter(owner=request.user).exists()
        else:
            context['shop_exists'] = False
    else:
        context['is_buyer'] = False
        context['is_seller'] = False
        context['shop_exists'] = False

    return context
