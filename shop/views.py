from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ProductForm, UpdateStockForm
from .models import Product, ProductCategory, Shop
from django.db.models import Q

@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'shop/seller_dashboard.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        form = UpdateStockForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')  # Redirect to dashboard after update
    else:
        form = UpdateStockForm(instance=product)

    return render(request, 'shop/update_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
    return redirect('seller_dashboard')

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
    return render(request, 'shop/buyer_home.html', context)



