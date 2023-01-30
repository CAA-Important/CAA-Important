from django.views.generic import TemplateView

from django.shortcuts import render

# Create your views here.

class HelloInfoView(TemplateView):
    template_name = "hello/hello_info.html"

    def get(self, request):
        return render(request, self.template_name)

class HelloAppView(TemplateView):
    template_name = "hello/hello_app.html"

    def get(self, request):

        oldval = request.COOKIES.get('zap', None)

        if oldval :
            num_visits = request.session.get('num_visits', 0) + 1 # No expired date = until browser close

        else :
            num_visits = 1 # No expired date = until browser close

        # I know it's typically bad practice to change data based on a GET
        # request.  But the data in question is essentially "number of
        # times a GET request has been sent for this page," so it feels like a
        # meaningful excception to the rule.
        request.session['num_visits'] = num_visits

        return render(request, self.template_name)




