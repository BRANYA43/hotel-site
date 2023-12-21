from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from accounts import forms

User = get_user_model()


class UserRegisterView(generic.FormView):
    model = User
    template_name = 'accounts/register_form.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('accounts:user-register-first-success')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
