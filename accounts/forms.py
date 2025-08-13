from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from housesell.models import Testimonial

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    profession = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Créer ou mettre à jour le profil
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            profile.profession = self.cleaned_data.get('profession', '')
            profile.location = self.cleaned_data.get('location', '')
            profile.save()
        
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'phone', 'date_of_birth', 'profession', 'website', 'facebook', 'twitter', 'linkedin']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Partagez votre expérience avec SellHub...'}),
            'rating': forms.Select(choices=[(i, f'{i} étoile{"s" if i > 1 else ""}') for i in range(1, 6)]),
        }

