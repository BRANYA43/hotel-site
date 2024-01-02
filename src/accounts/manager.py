from django.contrib.auth.base_user import BaseUserManager

EMAIL_ERROR_MESSAGE = 'Email must be'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        return self._create_user(email, password, **extra_field)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['email_is_confirmed'] = True
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError(EMAIL_ERROR_MESSAGE)
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self.db)
        return user
