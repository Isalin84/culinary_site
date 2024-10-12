from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Comment
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

def home(request):
    dishes = Dish.objects.all()
    return render(request, 'recipes/home.html', {'dishes': dishes})

def dish_detail(request, id):
    dish = get_object_or_404(Dish, id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            Comment.objects.create(dish=dish, user=request.user, text=text)
            return redirect('dish_detail', id=dish.id)
        else:
            return redirect('login')
    comments = dish.comments.all()
    return render(request, 'recipes/dish_detail.html', {'dish': dish, 'comments': comments})

# Создание пользовательской формы регистрации с добавлением классов Bootstrap
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Создание пользовательской формы аутентификации с добавлением классов Bootstrap
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
