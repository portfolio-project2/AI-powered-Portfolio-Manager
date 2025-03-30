from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'manager/home.html')


def dashboard(request):
    return render(request, 'manager/dashboard2.html')

def market_news(request):
    return render(request, 'manager/market_news.html')

def financial_goals(request):
    return render(request, 'manager/financial-goals.html')


def recommendations(request):
    return render(request, 'manager/recommendations.html')

def help_center(request):
    return render(request, 'manager/help.html')