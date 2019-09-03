import logging

from django.core.management.base import BaseCommand
from django.conf import settings
import kombu
import kombu.mixins

from app import models


log = logging.getLogger(__name__)


class Consumer(kombu.mixins.ConsumerMixin):
    def __init__(self, connection, queue_name):
        self.queue = kombu.Queue(queue_name)
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer([self.queue], callbacks=[self.on_message])]

    def on_message(self, body, message):
        provider_slug = message.headers["X-Provider"]
        log.info(f"Received {provider_slug} transaction.")
        models.Transaction(provider_slug=provider_slug, payload=body).save()
        message.ack()


class Command(BaseCommand):
    help = "Consume auth transactions from the specified queue"

    def add_arguments(self, parser):
        parser.add_argument("queue_name")

    def handle(self, *args, **options):
        self.stdout.write(f"Consuming from {options['queue_name']}")
        conn = kombu.Connection(settings.AMQP_DSN)

        try:
            Consumer(conn, options["queue_name"]).run()
        except KeyboardInterrupt:
            self.stdout.write("Shutting down.")
