import json
import time

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def publish_transaction_event(transaction):
    event = {
        'id': str(transaction.id),
        'from_account': str(transaction.from_account.id),
        'to_account': str(transaction.to_account.id),
        'amount': float(transaction.amount),
        'created_at': transaction.created_at.isoformat()
    }
    producer.send('transactions', event)


for _ in range(10):
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        break
    except NoBrokersAvailable:
        time.sleep(5)
