from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from contact.models import Contact
from django.core.validators import EmailValidator, MinLengthValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from contact.models import CustomUser
from django.contrib.auth import authenticate, login
import re



class RegisterPageForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            # Only do something if both fields are valid so far.
            if password1 != password2:
                raise ValidationError("password do not match")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash the password
        if commit:
            user.save()
        return user


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email  already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

class LoginPageForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), label="Email")
    password = forms.CharField(label="Password",strip=False,widget=forms.PasswordInput,)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
               raise forms.ValidationError("The username or password is incorrect Note: both fields  maybe case-sensitive!!!!!!")
            # if user.check_password(password):
            #     raise ValidationError("The username or password is incorrect Note: both fields  maybe case-sensitive!!!!!!")
        return cleaned_data      



class ProfileChangeForm(forms.ModelForm):
    phone_number = forms.CharField(required=False,)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        if new_email and new_email != self.instance.email:
            if CustomUser.objects.filter(email=new_email).exists():
                raise ValidationError("Email already exixts")
        return new_email 

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Prefer not to say')
]


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)  # RadioSelect for radio buttons
    class Meta:
        model = CustomUser
        fields = ("email","first_name","last_name", "phone_number","gender")    
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if CustomUser.objects.filter (phone_number=phone_number).exists():
            raise ValidationError ("phone_number already in use")
        return phone_number


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email","password", 'phone_number')

class UploadFileForm(forms.Form):
    profile_picture = forms.FileField(required=False, label="upload picture")
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

