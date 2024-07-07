from django.shortcuts import render
from django.views.generic import FormView, View
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'registration.html'
    form_class = UserRegisterForm
    
    def get_success_url(self):
        return reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form) # form_valid function call hobe jodi sob thik thake
    
class UserUpdateView(View):
    template_name = 'profile.html'
    success_url = 'profile'

    def get(self, request):
        form = UserUpdateForm(instance=self.request.user)
        return render(self.request, self.template_name, {'form':form})
    
    def post(self, request):
        form = UserUpdateForm(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
  
class UserLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('profile')

# class UserLogoutView(LogoutView):
#     next_page = reverse_lazy('homepage')

def logOut(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('homepage')