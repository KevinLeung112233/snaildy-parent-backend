from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def create_booking_statuses(sender, **kwargs):
    if sender.name == 'booking':
        BookingStatus = apps.get_model('booking', 'BookingStatus')
        statuses = ['pending', 'confirmed',
                    'canceled', 'paid', 'completed', 'no-show']
        for status in statuses:
            BookingStatus.objects.get_or_create(status=status)
