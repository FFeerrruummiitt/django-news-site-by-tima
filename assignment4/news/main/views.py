from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import re
from .models import *
from django.contrib import messages
from .forms import  CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def registerPage(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            pas1 = form.cleaned_data.get('password1')
            pas2 = form.cleaned_data.get('password2')
            messages.success(request, 'Account was created for '+ user)
            print('good')
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username OR password is incorrect')

    context = {}
    return render(request,'accounts/login.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login')
def home(request):
    first_news = News.objects.first()
    three_news = News.objects.all()[1:5]
    three_categories = Category.objects.all()[0:3]
    return render(request,'home.html',{
        'first_news':first_news,
        'three_news':three_news,
        'three_categories':three_categories
    })
def all_news(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter 'q'
    all_news = News.objects.all()

    if query:
        all_news = all_news.filter(title__icontains=query)  # Filter the news by the search query

    return render(request, 'all-news.html', {
        'all_news': all_news,
        'query': query  # Pass the query back to the template for display
    })

def detail(request, id):
    news = News.objects.get(pk=id)
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['message']
        Comments.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment
        )
        messages.success(request, 'Comment sended successfully')
    rel_news = News.objects.filter(category=news.category).exclude(id=id)
    comments = Comments.objects.filter(news=news,status=True).order_by('-id')
    return render(request, 'detail.html', {
        'news':news,
        'related_news':rel_news,
        'comments':comments
    })
def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category.html',{
        'cats':cats
    })
def category(request, id):
    category = Category.objects.get(pk=id)
    news = News.objects.filter(category=category)
    return render(request, 'category-news.html', {
        'all_news':news,
        'category':category,
    })

def proflie(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('login')
