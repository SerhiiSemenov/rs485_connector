import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import devices_mapping
from do_controller import DOController as do_ctrl

do_controllers_array = dict()
is_inprogress = True


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
            do_controllers_array[devices_mapping.map_table[message.topic][1]].channel_on(devices_mapping.map_table[message.topic][2])

        else:
            print("Exec: {}; ID {}; Port {}".format(devices_mapping.map_table[message.topic][0],
                                                    devices_mapping.map_table[message.topic][1],
                                                    devices_mapping.map_table[message.topic][2]))
            do_controllers_array[devices_mapping.map_table[message.topic][1]].channel_off(devices_mapping.map_table[message.topic][2])


def connect_to_broker():
    #broker_address="127.0.0.1"
    broker_address = "192.168.0.113"
    print("creating new instance")
    client = mqtt.Client("RS485_client")    # create new instance
    client.on_message = on_message          # attach function to callback
    print("connecting to broker")
    client.connect(broker_address)          # connect to broker
    client.loop_start()                     # start the loop
    print("Subscribing to topics")
    for topic_name in devices_mapping.map_table:
        client.subscribe(topic_name)

    # client.loop_forever(retry_first_connection=True)


def main():
    print("Run app")
    do_controllers_array[0x3] = do_ctrl(slave_id=0x3)
    time.sleep(1)
    do_controllers_array[0x4] = do_ctrl(slave_id=0x4)
    time.sleep(1)
    connect_to_broker()
    ping_controller_timeout = 0

    while is_inprogress:
        time.sleep(1)
        # ping_controller_timeout = ping_controller_timeout+1
        # if ping_controller_timeout > 10000:
        #     ping_controller_timeout = 0
        #     print("Ping ethToRS server ")
        #     do_controllers_array[0x3].get_channel_status(0x1)


if __name__ == "__main__":
    main()