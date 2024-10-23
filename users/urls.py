from django.urls import path
from .import views
from users.views import RegisterPageView, LoginPageView, ProfileChangeView,UploadFileView
app_name = 'users'

urlpatterns = [
    path("register/", RegisterPageView.as_view(), name="register"),
    path("upload/", UploadFileView.as_view(), name="picture"),

    path("login/", LoginPageView.as_view(), name="login"),
    path("profile/",views.ProfileChangeView.as_view(), name="profile_change" ),
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),

     path('github/login/', views.github_login, name='github_login'),
    path('github/callback/', views.github_callback, name='github_callback'),
    path('facebook/login/', views.facebook_login, name='facebook_login'),
    path('facebook/callback/', views.facebook_callback, name='facebook_callback'),
]