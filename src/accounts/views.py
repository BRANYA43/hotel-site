from django.contrib.auth import get_user_model, login, mixins, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic

from accounts import forms
from accounts.models import Profile

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


class UserRegisterSuccessView(generic.TemplateView):
    template_name = 'accounts/register_success.html'


class UserConfirmEmailView(generic.View):
    token_generator = default_token_generator
    success_url = reverse_lazy('accounts:user-confirm-email-success')
    failure_url = reverse_lazy('accounts:user-confirm-email-failure')

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if self.token_generator.check_token(user, token):
            user.email_is_confirmed = True
            user.save()
            return HttpResponseRedirect(self.success_url)
        return HttpResponseRedirect(self.failure_url)

    def get_user(self, uidb64):
        try:
            user_pk = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class UserConfirmEmailSuccessView(generic.TemplateView):
    template_name = 'accounts/confirm_email_success.html'


class UserConfirmEmailFailureView(generic.TemplateView):
    template_name = 'accounts/confirm_email_failure.html'


class UserLoginView(generic.FormView):
    form_class = forms.UserLoginForm
    success_url = reverse_lazy('accounts:user-account')
    template_name = 'accounts/login_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserLogoutView(mixins.LoginRequiredMixin, generic.View):
    success_url = reverse_lazy('accounts:user-login')

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(self.success_url)


class UserRegisterContinueView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = forms.UserRegisterContinueForm
    template_name = 'accounts/register_continue_form.html'
    success_url = reverse_lazy('accounts:user-account')

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserAccountView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = forms.UserAccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:user-account')
    register_continue_url = reverse_lazy('accounts:user-register-continue')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile.has_necessary_data:
            return HttpResponseRedirect(self.register_continue_url)
        else:
            return super().get(request, *args, **kwargs)
