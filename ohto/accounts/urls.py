from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.contrib.auth import views as auth_views
from .views import template_views,views
urlpatterns = [
    path('mypage/',views.MyPageView.as_view(),name='mypage'),
    path('signup/', views.SignUpView.as_view(),name='signup'),
    path('login/',template_views.login,name='login'),
    path('logout/',template_views.logout,name='logout'),
    path('password_change',template_views.change_password,name='change_password'),
    path('profile_edit',template_views.profile_edit,name='profile_edit')
]

#NOTE: jwt token url
urlpatterns+=[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]