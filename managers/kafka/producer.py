from datetime import datetime
import json
from kafka import KafkaProducer
import random
import time

# Create producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def generate_order():
    products = ['laptop', 'phone', 'tablet', 'headphones', 'smartwatch']
    return {
        'order_id': random.randint(1000, 9999),
        'product': random.choice(products),
        'quantity': random.randint(1, 5),
        'price': round(random.uniform(100, 2000), 2),
        'timestamp': datetime.now().isoformat()
    }

def send_orders():
    while True:
        order = generate_order()
        producer.send('orders', value=order)
        print(f"Sent order: {order}")

        producer.flush()
        time.sleep(1)
    
if __name__ == "__main__":
    print(f"Starting producer ...")
    send_orders()