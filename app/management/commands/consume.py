import logging

from django.core.management.base import BaseCommand
from django.conf import settings
import kombu
import kombu.mixins

from app import models


QUEUE_NAMES = ["amex-auth", "mastercard-auth", "visa-auth", "visa-settlement"]


log = logging.getLogger(__name__)


class Consumer(kombu.mixins.ConsumerMixin):
    def __init__(self, connection):
        self.queues = [kombu.Queue(queue_name) for queue_name in QUEUE_NAMES]
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(self.queues, callbacks=[self.on_message])]

    def on_message(self, body, message):
        provider_slug = message.headers["X-Provider"]
        log.info(f"Received {provider_slug} transaction.")
        models.Transaction(provider_slug=provider_slug, payload=body).save()
        message.ack()


class Command(BaseCommand):
    help = "Consume auth transactions from the specified queue"

    def handle(self, *args, **options):
        self.stdout.write(f"Consuming from queues: {', '.join(QUEUE_NAMES)}")
        conn = kombu.Connection(settings.AMQP_DSN)

        try:
            Consumer(conn).run()
        except KeyboardInterrupt:
            self.stdout.write("Shutting down.")
