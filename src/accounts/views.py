from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic

from accounts import forms

User = get_user_model()


class UserRegisterView(generic.FormView):
    model = User
    template_name = 'accounts/register_form.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('accounts:user-register-success')

    subject_template_name = 'accounts/subject_of_register_data_confirmation.html'
    body_template_name = 'accounts/body_of_register_data_confirmation.html'
    token_generator = default_token_generator

    def form_valid(self, form):
        user = form.save()
        self.send_mail(user)
        return super().form_valid(form)

    def send_mail(self, user):
        current_site = get_current_site(self.request)
        subject = self._get_mail_subject(current_site)
        body = self._get_mail_body(current_site, user)
        send_mail(subject, body, None, [user.email])

    def _get_mail_subject(self, current_site: RequestSite):
        context = self._get_mail_subject_context(current_site)
        subject = loader.render_to_string(self.subject_template_name, context)
        subject = ''.join(subject.splitlines())
        return subject

    def _get_mail_body(self, current_site: RequestSite, user):
        context = self._get_mail_body_context(current_site, user)
        return loader.render_to_string(self.body_template_name, context)

    def _get_mail_subject_context(self, current_site: RequestSite) -> dict:
        return {'site_name': current_site.name}

    def _get_mail_body_context(self, current_site: RequestSite, user) -> dict:
        return {
            'site_name': current_site.name,
            'domain': current_site.domain,
            'protocol': 'https' if self.request.is_secure() else 'http',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': self.token_generator.make_token(user),
        }
