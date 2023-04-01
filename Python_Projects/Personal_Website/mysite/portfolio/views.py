from django.shortcuts import render
from django.views import View
from django.conf import settings

# Create your views here.

class PortfolioView(View):
    def get(self, request):
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed': settings.INSTALLED_APPS,
            'islocal': islocal
        }
        return render(request, 'portfolio/portfolio_main.html', context)