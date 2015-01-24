from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page


class HomeView(TemplateView):
    template_name = 'pages/home.html'

home = cache_page(60 * 10)(HomeView.as_view())
