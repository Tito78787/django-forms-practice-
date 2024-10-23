from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import FormView, CreateView
from django.utils import timezone
from requests import request
from .forms import RegisterPageForm,LoginPageForm,ProfileChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User 
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomUserCreationForm, CustomUserChangeForm,UploadFileForm
from contact.models import CustomUser
import requests
from django.conf import settings
import os
import config


# GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
# GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

GOOGLE_CLIENT_ID = config.FACEBOOK_CLIENT_ID
GOOGLE_CLIENT_SECRET = config.FACEBOOK_CLIENT_SECRET
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/google/callback/"
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URI = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"





class RegisterPageView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('contact:home')
    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data.get('email')
        phone_number = form.cleaned_data.get('phone_number')
        return super().form_invalid(form)
    

class LoginPageView(FormView):
    template_name = 'users/login.html'
    form_class = LoginPageForm
    def get_success_url(self):
        return reverse('users:profile_change')
 
    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            # Redirect to a success page.
            return redirect('users:profile_change')
        return super().form_invalid(form)


class ProfileChangeView(LoginRequiredMixin,UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileChangeForm
    def get_success_url(self):
        return reverse('users:profile_change')

    def get_object(self):
        # Return the user instance for the logged-in user
        return self.request.user



def google_login(request):
    # Step 1: Redirect user to Google's OAuth 2.0 server
    google_auth_url = (
        f"{GOOGLE_AUTH_URI}?response_type=code&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}&scope=email profile"
    )
    return redirect(google_auth_url)

def google_callback(request):
    # Step 2: Handle Google's callback and exchange code for an access token
    code = request.GET.get("code")
    token_response = requests.post(
        GOOGLE_TOKEN_URI,
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return HttpResponse("Authentication failed", status=401)

    # Step 3: Use the token to get user information from Google
    user_info_response = requests.get(
        GOOGLE_USER_INFO_URI,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_info = user_info_response.json()
    
    # Correct the key names for the user data
    email = user_info.get("email")
    first_name = user_info.get("given_name")  # Correct key for first name
    last_name = user_info.get("family_name")  # Correct key for last name

    # Google OAuth does not return a password, so generate a default one
    password = CustomUser.objects.make_random_password()

    # Step 4: Check if user exists in your database or create a new user
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        # Create a new user if it doesn't exist
        user = CustomUser.objects.create_user(email=email,first_name=first_name,last_name=last_name, password=password,  # You can set this to a random password or a default one
        )

    # Step 5: Log the user in
    login(request, user)
    return redirect('users:profile_change')


###github login#############

def github_login(request):
    client_id = settings.GITHUB_CLIENT_ID
    redirect_uri = settings.GITHUB_REDIRECT_URI
    authorization_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user'
    return redirect(authorization_url)

def github_callback(request):
    # Step 2: Exchange code for access token
    code = request.GET.get("code")
    
    token_response = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},  # Ensure response is in JSON
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.GITHUB_REDIRECT_URI
        },
    )
    
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        return HttpResponse("Authentication failed", status=401)

    # Step 3: Use the access token to get user info from GitHub
    user_info_response = requests.get(
        'https://api.github.com/user',
        headers={"Authorization": f"token {access_token}"},
    )
    
    user_info = user_info_response.json()
    
    # Extract the necessary user information
    email = user_info.get("email")
    username = user_info.get("login")  # GitHub username
    first_name = username
    # If email is missing (common for GitHub), you may need to handle this case
    if not email:
        email = f'{username}@github.com'  # Placeholder email

    # Step 4: Check if the user exists or create a new user
    try:
        user = CustomUser.objects.get(email=email, first_name=first_name,)
    except CustomUser.DoesNotExist:
        # If the user doesn't exist, create a new one
        user = CustomUser.objects.create_user(
            email=email,
            first_name = first_name,
            password=CustomUser.objects.make_random_password()  # GitHub handles authentication, no need for real password
        )
    
    # Step 5: Log the user in
    login(request, user)
    
    # Step 6: Redirect the user to their profile or another page
    return redirect('users:profile_change')







# Step 1: Facebook Login Redirect
def facebook_login(request):
    facebook_login_url = f"{settings.FACEBOOK_OAUTH_URL}?client_id={settings.FACEBOOK_CLIENT_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URI}&scope=email"
    return redirect(facebook_login_url)

# Step 2: Facebook Callback to Handle OAuth
def facebook_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Error: Missing code from Facebook", status=400)
    
    # Exchange code for access token
    token_response = requests.get(
        settings.FACEBOOK_TOKEN_URL,
        params={
            'client_id': settings.FACEBOOK_CLIENT_ID,
            'client_secret': settings.FACEBOOK_CLIENT_SECRET,
            'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
            'code': code
        }
    )
    
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    
    if not access_token:
        return HttpResponse("Authentication failed", status=401)

    # Fetch user information from Facebook
    user_info_response = requests.get(
        settings.FACEBOOK_USER_INFO_URL,
        params={'access_token': access_token}
    )
    user_info = user_info_response.json()

    # Extract the necessary user information
    email = user_info.get("email")
    first_name = user_info.get("surname")  # Fixing the field name
    last_name = user_info.get("last_name")
    phone_number = user_info.get("phone_number")
    # If email is missing, provide a fallback (sometimes Facebook doesn't return email)
    if not email:
        email = f'{first_name.lower()}.{last_name.lower()}@facebook.com'  # Placeholder email

    if not first_name:  # Ensure first_name is not empty
        first_name = "Titus"
        last_name = "Gikonyo"
        phone_number = "+254 745678789"
    # Step 4: Check if the user exists or create a new user
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        # If the user doesn't exist, create a new one
        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name or '',
            password=CustomUser.objects.make_random_password()  # Facebook handles authentication, no need for real password
        )
    
    # Step 5: Log the user in
    login(request, user)
    
    # Step 6: Redirect the user to their profile or another page
    return redirect('users:profile_change')

class UploadFileView(FormView):
    template_name = 'users/picture.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('contact:home')
    def form_valid(self, form):
        picture = form.cleaned_data.get("picture")
        return super().form_invalid(form)