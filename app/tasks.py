from celery import current_app

from app.serializers import TransactionSerializer


@current_app.task(name='auth-transactions.save')
def save_transaction(data: dict) -> None:
    serializer = TransactionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
