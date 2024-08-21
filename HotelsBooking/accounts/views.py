from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView#, UpdateView
from .models import Profile


# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.add_message(self.request, messages.WARNING, "Please enter username and password or sign up to proceed.")
        # messages.warning(self.request, "Please enter username and password or sign up to proceed.")
        return redirect('login')


class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "registration/profile_detail.html"

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
