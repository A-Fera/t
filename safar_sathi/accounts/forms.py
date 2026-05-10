from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, LocalGuide

WIDGET = {'class': 'form-control'}
SELECT = {'class': 'form-select'}

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={**WIDGET, 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={**WIDGET, 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={**WIDGET, 'placeholder': 'Email address'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={**WIDGET, 'placeholder': 'Username'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'language_preference', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs=WIDGET),
            'last_name': forms.TextInput(attrs=WIDGET),
            'email': forms.EmailInput(attrs=WIDGET),
            'language_preference': forms.TextInput(attrs=WIDGET),
            'profile_picture': forms.ClearableFileInput(attrs=WIDGET),
        }

class GuideForm(forms.ModelForm):
    user_first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs=WIDGET))
    user_last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs=WIDGET))
    user_username = forms.CharField(max_length=150, widget=forms.TextInput(attrs=WIDGET))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs=WIDGET))

    class Meta:
        model = LocalGuide
        fields = ['languages', 'contact_info', 'region', 'description', 'experience_years',
                  'hourly_rate', 'phone', 'guide_photo', 'references']
        widgets = {
            'languages': forms.TextInput(attrs=WIDGET),
            'contact_info': forms.TextInput(attrs=WIDGET),
            'region': forms.TextInput(attrs=WIDGET),
            'description': forms.Textarea(attrs={**WIDGET, 'rows': 4}),
            'experience_years': forms.NumberInput(attrs=WIDGET),
            'hourly_rate': forms.NumberInput(attrs=WIDGET),
            'phone': forms.TextInput(attrs=WIDGET),
            'references': forms.Textarea(attrs={**WIDGET, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'user_first_name': instance.user.first_name,
                'user_last_name': instance.user.last_name,
                'user_username': instance.user.username,
                'user_email': instance.user.email,
            })
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
