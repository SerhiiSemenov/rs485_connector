import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import devices_mapping


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if message.topic in devices_mapping.map_table:
        if str(message.payload.decode("utf-8")) == "ON":
            print("Exec: {}; ID {}; Port {}".format(devices_mapping.map_table[message.topic][0],
                                                devices_mapping.map_table[message.topic][1],
                                                devices_mapping.map_table[message.topic][2]))


def connect_to_broker():
    broker_address="127.0.0.1"
    print("creating new instance")
    client = mqtt.Client("RS485_client")    # create new instance
    client.on_message=on_message            # attach function to callback
    print("connecting to broker")
    client.connect(broker_address)          # connect to broker
    client.loop_start()                     # start the loop
    print("Subscribing to topics")
    for topic_name in devices_mapping.map_table:
        client.subscribe(topic_name)

    # client.loop_forever(retry_first_connection=True)
    while True:
        time.sleep(1)


def main():
    print("Run app")
    connect_to_broker()


if __name__ == "__main__":
    main()