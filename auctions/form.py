from django import forms

class new_listing_form(forms.Form):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-3'}),label='Product name', max_length=64)
    img_product = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control mt-3'}),label='Img URL', required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-3'}), label="Description")
    start_bit = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control mt-3'}), label="Start Bid")

class submit_bid_form(forms.Form):
    bid = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control mt-3'}), label='', min_value=0)

class comment_form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-3'}), label="")