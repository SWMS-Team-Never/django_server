from django.urls import path
from search_music import views

urlpatterns = [
    path('', views.SearchView.as_view())
]