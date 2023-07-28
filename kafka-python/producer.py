from confluent_kafka import Producer
from config import config


def callback(err, event):
    if err:
        print(f"Produce to topic {event.topic()} failed for event: {event.key()}")
    else:
        val = event.value().decode("utf8")
        print(f"{val} sent to partition {event.partition()}.")


def say_hello(producer, key):
    value = f"hello {key}!"
    producer.produce("hello_topic", value, key, on_delivery=callback)


if __name__ == "__main__":
    producer = Producer(config)
    keys = ["amy", "brenda", "cindy", "derrick", "elaine", "Fred", "amy", "vincent"]
    [say_hello(producer, key) for key in keys]
    producer.flush()
