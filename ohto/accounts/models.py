from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class User(AbstractUser):
    #장고3에서 필드에 선택할 수있는 값 미리 지정한다.
    phone_number = models.CharField(max_length=40,validators=[RegexValidator(r"^010-?\d{4}-?\d{4}$")],blank=True)
    avatar = models.ImageField(blank=True,upload_to = "accounts/profile/%Y/%m"
    ,help_text="48*48 크기의 png/jpeg파일을 업로드해주세요")
    #django imagekit 라이브러리 이용하여 이미지 처리 할수있다.
    email=models.EmailField(unique=True,blank=True)
    #NOTE: 속성 변경으로 필드 수정후에 .save() 호출해야 database hit 일어남
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    @name.setter
    def name(self,name):
        f_name,l_name = name
        self.first_name=f_name
        self.last_name = l_name
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 1

