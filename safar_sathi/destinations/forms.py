from django import forms
from .models import Destination, Photo

W = {'class': 'form-control'}
S = {'class': 'form-select'}

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'location', 'state', 'country', 'category',
                  'best_time_to_visit', 'entry_fee', 'latitude', 'longitude', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs=W),
            'description': forms.Textarea(attrs={**W, 'rows': 5}),
            'location': forms.TextInput(attrs=W),
            'state': forms.TextInput(attrs=W),
            'country': forms.TextInput(attrs=W),
            'category': forms.Select(attrs=S),
            'best_time_to_visit': forms.TextInput(attrs=W),
            'entry_fee': forms.NumberInput(attrs=W),
            'latitude': forms.NumberInput(attrs=W),
            'longitude': forms.NumberInput(attrs=W),
        }

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs=W),
            'caption': forms.TextInput(attrs={**W, 'placeholder': 'Optional caption'}),
        }
