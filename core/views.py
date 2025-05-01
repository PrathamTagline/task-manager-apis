from django.shortcuts import render


def dashboard_page_view(request):
    return render(request, 'core/dashboard_page.html')

def home_view(request):
    return render(request, 'core/home_page.html')