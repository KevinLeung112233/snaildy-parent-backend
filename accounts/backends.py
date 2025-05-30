# accounts/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        # Get credentials
        email = kwargs.get('email')
        phone_number = kwargs.get('phone_number')
        password = kwargs.get('password')

        # Determine which identifier to use
        if email:
            lookup = {'email': email}
        elif phone_number:
            lookup = {'phone_number': phone_number}
        else:
            return None  # No valid identifier

        try:
            user = UserModel.objects.get(**lookup)

            # Check password and active status
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            return None  # User not found

        return None  # Password didn't match
