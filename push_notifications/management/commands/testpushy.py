from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Testing tool for sending pushy push notification.'

    def handle(self, *args, **kwargs):
        from push_notifications.models import PushyDevice

        device_token = None
        for arg in args:
            device_token = arg
            break

        device = PushyDevice(
            registration_id=device_token
        )

        try:
            device.send_message('Hello pushy!')
            self.stdout.write('Message sent!')
        except Exception, ex:
            self.stderr.write(str(ex))
