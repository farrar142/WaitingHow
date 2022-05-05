from django import forms
from .models import Shop

class ShopRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['zipNo'].required = True
        self.fields['address'].required = True
        self.fields['detailAddress'].required = True
        self.fields['lat'].required = True
        self.fields['lng'].required = True

    class Meta:
        model = Shop
        fields = ['name','bizNum','zipNo','address','detailAddress','lat','lng']