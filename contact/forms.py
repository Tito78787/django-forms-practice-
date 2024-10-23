from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from contact.models import Contact
from django.core.validators import EmailValidator, MinLengthValidator
from django.contrib.auth.models import User
from contact.models import CustomUser
from django.core.exceptions import ValidationError



class ContactPageForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','message']
    name = forms.CharField()
    email = forms.EmailField(required=True, validators=[EmailValidator(message="Enter a valid email address.")])
    message = forms.CharField(widget=forms.Textarea, required=True, validators=[MinLengthValidator(10, message="The message must be at least 10 characters long.")])


    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if the email already exists in the User model
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already exist")
        return email