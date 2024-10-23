from django.shortcuts import render
from django.views.generic.base import TemplateView
from django import forms
from .forms import ContactPageForm
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import FormView


class ContactPageView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactPageForm
    success_url = reverse_lazy('contact:home')

    def form_valid(self, form):
        user = form.save()
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        return super().form_valid(form)