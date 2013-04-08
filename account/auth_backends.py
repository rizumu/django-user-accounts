from django.db.models import Q

try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from account.future_1_5 import get_user_model
from django.contrib.auth.backends import ModelBackend

from account.models import EmailAddress


class UsernameAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        User = get_user_model()
        try:
            user = User.objects.get(username__iexact=credentials["username"])
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user


class EmailAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        qs = EmailAddress.objects.filter(Q(primary=True) | Q(verified=True))
        try:
            email_address = qs.get(email__iexact=credentials["username"])
        except EmailAddress.DoesNotExist:
            return None
        else:
            user = email_address.user
            if user.check_password(credentials["password"]):
                return user
