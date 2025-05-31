from django.shortcuts import render

def home_view(request):
    """View for the home page"""
    return render(request, 'core/home.html')

def culture_view(request):
    """View for the culture page"""
    return render(request, 'core/culture.html')

def geography_view(request):
    """View for the geography page"""
    return render(request, 'core/geography.html')

def history_view(request):
    """View for the history page"""
    return render(request, 'core/history.html')
