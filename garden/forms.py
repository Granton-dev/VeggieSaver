from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vegetable, WasteLog

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class VegetableForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ['name', 'variety', 'planted_date', 'quantity', 'location', 'notes', 'photo', 'health_status']
        widgets = {
            'planted_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class WasteLogForm(forms.ModelForm):
    class Meta:
        model = WasteLog
        fields = ['vegetable', 'vegetable_name', 'quantity_wasted', 'reason', 'notes', 'date']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vegetable'].queryset = Vegetable.objects.filter(user=user)
        self.fields['vegetable'].required = False