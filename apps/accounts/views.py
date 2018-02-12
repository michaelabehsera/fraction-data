from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.shortcuts import redirect

from .forms import SignUpForm


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)

        return redirect(self.success_url)
