from django.urls import path
from contact.views import ContactPageView

app_name = 'contact' 
urlpatterns = [
    path("", ContactPageView.as_view(), name="home"),

]