from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (LoginView,logout_then_login, PasswordChangeView as AuthPasswordChange)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from ..forms import SignUpForm,ProfileForm,PasswordChangeForm
# Create your views here.

def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST,req.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(req,'회원가입을 환영하오')
            auth_login(req,user)
            next_url = req.GET.get('next','/')
            return redirect(next_url)
    else:
        form = SignUpForm()
    return render(req,'accounts/signup_form.html',{
        "form":form
    })

class CustomLoginView(LoginView):
    template_name='accounts/login_form.html'
    next_page = 'template_index'

#login = LoginView.as_view(template_name = 'accounts/login_form.html')
login = CustomLoginView.as_view()
def logout(req):
    messages.success(req,'로그아웃 되었소')
    return logout_then_login(req)

@login_required
def profile_edit(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST,req.FILES,instance = req.user)
        if form.is_valid():
            form.save()
            messages.success(req,'Profile 수정')
            return redirect('profile_edit')
    else:
        form= ProfileForm(instance=req.user)

    return render(req,'accounts/profile_edit_form.html',{
        "form":form
    })

class PasswordChangeView(LoginRequiredMixin,AuthPasswordChange):
    success_url = reverse_lazy('change_password')
    template_name = 'accounts/password_chage_form.html'
    form_class = PasswordChangeForm
    def form_valid(self,form):
        messages.success(self.request,'암호변경완료')
        return super().form_valid(form)
change_password = PasswordChangeView.as_view()

