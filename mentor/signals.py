import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings
from .models import Mentor


def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


@receiver(post_save, sender=Mentor)
def create_user_for_mentor(sender, instance, created, **kwargs):
    if created and not instance.user_id:
        username = f"mentor_{instance.pk}"
        password = generate_random_password()

        user = User.objects.create_user(
            username=username,
            email=instance.user.email if instance.user else '',
            password=password,
            is_staff=True,
            is_active=True,
        )
        instance.user = user
        instance.save()

        mentor_group, _ = Group.objects.get_or_create(name='Mentors')
        user.groups.add(mentor_group)
        user.save()

        # Send email with login credentials
        if user.email:
            subject = "您的導師帳號已建立"
            message = (
                f"您好，{username}，\n\n"
                f"您的導師帳號已建立。\n"
                f"登入帳號：{username}\n"
                f"初始密碼：{password}\n\n"
                "請盡快登入系統並更改您的密碼。\n\n"
                "謝謝！"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

        # Print password only in development environment
        if settings.DEBUG:
            print(
                f"Mentor user created: username={username}, password={password}")
