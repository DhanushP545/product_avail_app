from django.shortcuts import render,redirect, get_object_or_404
from .models import PreBooking, Product, ProductCategory, Shop, PreBooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def buyer_home(request):
    categories = ProductCategory.objects.all()
    featured_shops = Shop.objects.filter(is_featured=True)

    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )

    context = {
        'categories': categories,
        'featured_shops': featured_shops,
        'results': results,
        'query': query,
    }
    return render(request, 'booking/buyer_home.html', context)

from django.shortcuts import get_object_or_404

def view_category_products(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'booking/category_products.html', context)

def view_shop_products(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    products = Product.objects.filter(seller=shop.owner)

    context = {
        'shop': shop,
        'products': products,
    }
    return render(request, 'booking/view_shop_products.html', context)

@login_required
def prebook_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))  # default to 1 if not given
        
        if quantity <= 0:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('view_shop_products', shop_id=product.seller.id)
        
        if product.stock_quantity < quantity:
            messages.error(request, "Not enough stock available for prebooking.")
            return redirect('view_shop_products', shop_id=product.seller.id)

        PreBooking.objects.create(
            product=product,
            buyer=request.user,
            quantity=quantity,
            status='pending'
        )
        messages.success(request, "Your pre-booking request has been made and is pending approval ✅")
        return redirect('buyer_home')

    context = {
        'product': product,
    }
    return render(request, 'booking/prebook_product.html', context)



@login_required
def view_pre_bookings(request):
    pre_bookings = PreBooking.objects.filter(product__seller=request.user)  # Fetch pre-bookings for the seller's products
    return render(request, 'booking/pre_bookings.html', {'pre_bookings': pre_bookings})

def accept_prebooking(request, booking_id):
    print("reached")
    booking = get_object_or_404(PreBooking, id=booking_id, product__seller=request.user)
    product = booking.product

    if booking.status.lower() != 'pending':
        messages.warning(request, "This booking has already been processed.")
    elif product.stock_quantity >= booking.quantity:
        product.stock_quantity -= booking.quantity
        product.save()
        booking.status = 'ACCEPTED'
        booking.save()
        messages.success(request, "Booking accepted.")
    else:
        messages.error(request, "Not enough stock to accept this booking.")
    
    return redirect('view_pre_bookings')


def reject_booking(request, booking_id):
    pre_booking = get_object_or_404(PreBooking, id=booking_id)

    # Ensure the pre-booking is still in pending state before rejecting
    if pre_booking.status.lower() == 'pending' :
        pre_booking.delete()  # Delete the pre-booking
        return redirect('view_pre_bookings')  # Redirect back to the seller dashboard
    
    return redirect('view_pre_bookings')

from .models import PreBooking

@login_required
def confirm_prebooking(request, booking_id):
    booking = get_object_or_404(PreBooking, id=booking_id, product__seller=request.user)
    if request.method.lower() == 'post' and booking.status.lower() == 'accepted':
        booking.status = 'confirmed_sold'
        booking.save()
        messages.success(request, "Booking marked as sold.")
        booking.delete()
    return redirect('view_pre_bookings')

@login_required
def cancel_prebooking(request, booking_id):
    booking = get_object_or_404(PreBooking, id=booking_id, product__seller=request.user)
    if request.method.lower() == 'post' and booking.status.lower() == 'accepted':
        product = booking.product
        product.stock_quantity += booking.quantity
        product.save()
        booking.status = 'cancelled'
        booking.save()
        messages.error(request, "Booking cancelled. and stock restored.")
        booking.delete()
    return redirect('view_pre_bookings')

