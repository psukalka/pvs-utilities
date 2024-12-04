import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='order-processing-group',
    value_deserializer=lambda x:json.loads(x.decode('utf-8'))
)

def process_order(order):
    total_value = order['quantity'] * order['price']
    print(f"\nNew Order Received:")
    print(f"Order ID: {order['order_id']}")
    print(f"Product: {order['product']}")
    print(f"Quantity: {order['quantity']}")
    print(f"Total Value: ${total_value:.2f}")
    print(f"Timestamp: {order['timestamp']}")
    print("-" * 50)

def start_consumer():
    try:
        print(f"Starting consumer...")
        for message in consumer:
            process_order(message.value)
    except KeyboardInterrupt:
        print(f"Stopping consumer...")
        consumer.close()

if __name__ == "__main__":
    start_consumer()