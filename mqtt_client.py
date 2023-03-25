import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import devices_mapping
from do_controller import DOController as do_ctrl
import queue
import threading
import sys
import syslog

command_queue = queue.Queue()

do_controllers_array = dict()
is_inprogress = True


def worker(client):
    while True:
        item = command_queue.get()
        topic = item[0]
        payload = item[1]
        print(f'Working on {topic}')

        if topic in devices_mapping.map_table:
            if payload == "ON":
                print("Exec: {}; ID {}; Port {}".format(devices_mapping.map_table[topic][0],
                                                        devices_mapping.map_table[topic][1],
                                                        devices_mapping.map_table[topic][2]))
                do_controllers_array[devices_mapping.map_table[topic][1]].channel_on(devices_mapping.map_table[topic][2])
                if len(devices_mapping.map_table[topic]) == 4:
                    client.publish(devices_mapping.map_table[topic][3], 'ON')
                    client.loop()


            else:
                print("Exec: {}; ID {}; Port {}".format(devices_mapping.map_table[topic][0],
                                                        devices_mapping.map_table[topic][1],
                                                        devices_mapping.map_table[topic][2]))
                do_controllers_array[devices_mapping.map_table[topic][1]].channel_off(devices_mapping.map_table[topic][2])
                if len(devices_mapping.map_table[topic]) == 4:
                    client.publish(devices_mapping.map_table[topic][3], 'OFF')
                    client.loop()


def on_message(client, userdata, message):
    print("message payload= {} topic= {} qos= {} flag= {}".format(str(message.payload.decode("utf-8")), message.topic,
                                                                  message.qos, message.retain))
    item = message.topic, str(message.payload.decode("utf-8"))
    command_queue.put(item)


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

    return client


def main():
    print("Run app")
    do_controllers_array[0x3] = do_ctrl(slave_id=0x3)
    time.sleep(1)
    do_controllers_array[0x4] = do_ctrl(slave_id=0x4)
    time.sleep(1)
    do_controllers_array[0x5] = do_ctrl(slave_id=0x5)
    time.sleep(1)
    do_controllers_array[0x6] = do_ctrl(slave_id=0x6)
    mqtt_client = connect_to_broker()
    worker_thread = threading.Thread(target=worker, daemon=True, args=(mqtt_client, ))
    worker_thread.start()

    while is_inprogress:
        time.sleep(1)
        if not worker_thread.is_alive():
            syslog.syslog(syslog.LOG_ERR, "rs485_connector rebooted")
            sys.exit(1)
        # ping_controller_timeout = ping_controller_timeout+1
        # if ping_controller_timeout > 10000:
        #     ping_controller_timeout = 0
        #     print("Ping ethToRS server ")
        #     do_controllers_array[0x3].get_channel_status(0x1)
    # mqtt_client.loop_forever(retry_first_connection=True)
    command_queue.join()


if __name__ == "__main__":
    main()