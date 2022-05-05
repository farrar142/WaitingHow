from django import forms
from .models import *
class CategoryRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True

    class Meta:
        model = Category
        fields = ['name']
        
class MenuRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True

    class Meta:
        model = Menu
        fields = ['name']
        
class InfoRegisterForm(forms.ModelForm):
    
    class Meta:
        model = Info
        fields = ['image','content']