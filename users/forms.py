from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf import settings

from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(label='Birthday', initial="01-01-2002", widget=forms.DateInput, input_formats=settings.DATE_INPUT_FORMATS)
    
    class Meta:
        model = User
        fields = ('name', 'tag', 'email', 'date_of_birth', 'avatar', 'phone_number', 'password')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-1'
            visible.field.widget.attrs['placeholder'] = visible.name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-1'
            visible.field.widget.attrs['placeholder'] = visible.name

    def clean(self):
        if self.is_valid():
            phone_number = self.cleaned_data.get('phone_number')
            password = self.cleaned_data.get('password')
            if not authenticate(phone_number=phone_number, password=password):
                raise forms.ValidationError('Invalid Login')


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'tag', 'email', 'date_of_birth', 'avatar', 'phone_number', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name', 'tag', 'email', 'date_of_birth', 'avatar', 'phone_number', 'password', 'is_superuser')

    def clean_password(self):
        return self.initial['password']