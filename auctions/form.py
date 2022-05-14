from unicodedata import category
from django import forms

CATEGORIES_CHOICES = [
    (1, 'Fashion'),
    (2, 'Toys'),
    (3, 'Eletronics'),
    (4, 'Home'),
    (5, 'Others'),
]

class new_listing_form(forms.Form):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-3'}),label='Product name', max_length=64)
    img_product = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control mt-3'}),label='Img URL', required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-3'}), label="Description")
    start_bit = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control mt-3'}), label="Start Bid")
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select mt-3'}), label="Category", choices=CATEGORIES_CHOICES)

class submit_bid_form(forms.Form):
    bid = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control mt-3'}), label='', min_value=0)

class comment_form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-3'}), label="")