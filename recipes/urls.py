from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dish/<int:id>/', views.dish_detail, name='dish_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
