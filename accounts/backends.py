# accounts/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


UserModel = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs.get('email')
        phone_number = kwargs.get('phone_number')
        password = kwargs.get('password')

        user = None

        try:
            if email:
                # Case-insensitive email lookup
                user = UserModel.objects.get(email__iexact=email)
            elif phone_number:
                user = UserModel.objects.get(phone_number=phone_number)
            else:
                return None

            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            return None

        return None
