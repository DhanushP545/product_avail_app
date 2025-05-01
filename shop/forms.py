from django import forms
from .models import Product, Shop, ProductCategory


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'location', 'phone_number',]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Shop Name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.id} - {obj.name}"

class ProductForm(forms.ModelForm):
    category = CategoryChoiceField(
        queryset=ProductCategory.objects.all(),
        empty_label=None,
        label='Category'
    )
 
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'category', 'image']
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select a category"

class UpdateStockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock_quantity']

