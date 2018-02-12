from django.views.generic.base import TemplateView

from .mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'
