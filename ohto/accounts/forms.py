from django import forms
from django.contrib.auth.forms import (UserCreationForm,PasswordChangeForm as AuthPasswordChangeForm)
from .models import User

class SignUpForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','first_name','last_name']
    #장고에서는 username에만 unique 설정 되어있고 email은 그렇지 않다.
    #따라서 유효성 검사 로직을 작성한다.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email = email)
            if qs.exists():
                raise forms.ValidationError("이미 있는 이메일임")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','avatar']

class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self) -> str:
        old_password = self.cleaned_data.get('old_password')
        new_password_1 = self.cleaned_data.get('new_password1')
        if old_password and new_password_1:
            if old_password == new_password_1:
                raise forms.ValidationError('똑같은 암호다 변경해야하지 않겠나?')
        return new_password_1