from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'manager/home.html')


def help_center(request):
    return render(request, 'manager/help_center.html')


def dashboard(request):
    return render(request, 'manager/dashboard.html')

def news_data(request):
    
    return render(request, 'manager/news_data.html')