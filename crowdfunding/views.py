from django.shortcuts import render

def home_view(request):
    """Temporary home page view"""
    return render(request, 'base.html')