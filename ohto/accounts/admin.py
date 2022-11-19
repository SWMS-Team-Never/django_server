from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','is_active','is_superuser','is_staff','show_avatar']
    
    def show_avatar(self,user):
        if user.avatar:
            return mark_safe(f'<img src="{user.avatar_url}" style="width:70%"/>')
        return None


