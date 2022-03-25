import socket
import time
import errno
from umodbus import conf
from umodbus.client.serial import rtu
from umodbus.utils import recv_exactly
import sys
from serial import PARITY_NONE
from serial.rs485 import RS485, RS485Settings
import fcntl
import struct


class DOController:
    """Wrap basic Modbus operation with
    """

    def __init__(self, slave_id=0x1):
        self.slave_id = slave_id
        self.serial_port = RS485(  # instead of serial.serial_for_url
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=PARITY_NONE,
            stopbits=1, bytesize=8, timeout=1
        )
        # RS485Settings(delay_before_tx=0, delay_before_rx=0, rts_level_for_tx=True, rts_level_for_rx=False, loopback=False)

    def __del__(self):
        print("Close port")
        self.serial_port.close()

    def send_message(self, adu, serial_port):
        """ Send ADU over serial to to server and return parsed response.

        :param adu: Request ADU.
        :param sock: Serial port instance.
        :return: Parsed response from server.
        """
        serial_port.write(adu)
        serial_port.flush()
        time.sleep(.5)

        # Check exception ADU (which is shorter than all other responses) first.
        exception_adu_size = 5
        response_error_adu = recv_exactly(serial_port.read, exception_adu_size)
        rtu.raise_for_exception_adu(response_error_adu)

        expected_response_size = \
            rtu.expected_response_pdu_size_from_request_pdu(adu[1:-2]) + 3
        response_remainder = recv_exactly(
            serial_port.read, expected_response_size - exception_adu_size)

        return rtu.parse_response_adu(response_error_adu + response_remainder, adu)

    def channel_on(self, channel):
        print("Turn On channel {}".format(channel))
        message = rtu.write_single_register(slave_id=self.slave_id, address=channel, value=0x0100)
        response = self.send_message(message, self.serial_port)
        # self.serial_port.write(message)
        # self.serial_port.flush()
        # time.sleep(1)
        if response == 256:
            print("Success open rq")
        else:
            print("raw msg={}".format(message))
            print("response {}".format(response))
            print("Try to send command again")
            response = self.send_message(message, self.serial_port)

    def channel_off(self, channel):
        print("Turn Off channel {}".format(channel))
        message = rtu.write_single_register(slave_id=self.slave_id, address=channel, value=0x0200)
        response = self.send_message(message, self.serial_port)

        if response == 512:
            print("Success close rq")
        else:
            print("raw msg={}".format(message))
            print("response {}".format(response))
            print("Try to send command again")
            response = self.send_message(message, self.serial_port)

    def get_channel_status(self, channel):
        message = rtu.read_holding_registers(slave_id=self.slave_id, starting_address=channel, quantity=0x0001)
        print(message)
        response = self.send_message(message, self.serial_port)
        return response

    def get_slave_id(self):
        """slave_id=0xFF - broadcast messages"""
        message = rtu.read_holding_registers(slave_id=0xFF, starting_address=0xFF, quantity=0x0001)
        print(message)
        response = self.send_message(message, self.serial_port)
        print("response {}".format(response))
        return response

    def set_slave_id(self, new_id):
        message = self.write_single_register(slave_id=self.slave_id, address=0xFF, value=new_id)
        print(message)
        response = rtu.send_message(message, self.serial_port)
        print("response {}".format(response))
        return response


def main():

    controller_1 = DOController(slave_id=0x1)
    time.sleep(1)
    # controller_3 = DOController(slave_id=0x3)
    # time.sleep(1)
    # controller_4 = DOController(slave_id=0x4)
    # time.sleep(1)
    # Can be used just with one connected unit
    # print("Get ID")
    controller_1.get_slave_id()
    time.sleep(1)
    controller_1.get_slave_id()
    time.sleep(1)
    # controller_1.get_slave_id()
    # controller_1.set_slave_id(new_id=0x0001)
    # controller_1.get_slave_id()
    #
    for r in range(100):
        for i in range(1, 17):
            print("Out put id: {:02X}".format(i))
            controller_1.channel_on(i)
            # command = input("Press something for the continue\n")
            # if command == 'n':
            # elif command == 'e':

        for i in range(1, 17):
            print("Out put id: {:02X}".format(i))
            rsp = controller_1.get_channel_status(i)
            print(rsp)
            controller_1.channel_off(i)

    return 0

    # main program
    while True:
        command = input("Press something for the continue\n")
        print("Out put id: {0}".format(command))

        if command == '2':
            controller_4.channel_on(2)
            controller_4.channel_off(8)
            print('start loop')

            while(True):
                print('tune on')
                controller_4.channel_on(2)
                time.sleep(900)
                print('tune off')
                controller_4.channel_off(2)
                time.sleep(1800)

        if command == "test":
            while(True):
                print('lron')
                controller_4.channel_on(13)
                time.sleep(1)
                print('lroff')
                controller_4.channel_off(13)
                time.sleep(3)

        if command == 'kbon':
            controller_4.channel_on(6)
        if command == 'kboff':
            controller_4.channel_off(6)
        if command == '8':
            controller_4.channel_on(8)
            controller_4.channel_off(2)
        if command == '0':
            controller_4.channel_off(2)
            controller_4.channel_off(8)
        if command == 'bmlon':
            controller_4.channel_on(4)
        if command == 'bmloff':
            controller_4.channel_off(4)
        if command == 'ktlon':
            controller_4.channel_on(9)
        if command == 'ktloff':
            controller_4.channel_off(9)
        if command == 'klon':
            controller_4.channel_on(3)
        if command == 'kloff':
            controller_4.channel_off(3)
        if command == 'lron':
            controller_4.channel_off(1)
            controller_4.channel_on(13)
        if command == 'lroff':
            controller_4.channel_off(13)
            controller_4.channel_off(1)
        if command == 'lrhon':
            controller_4.channel_off(13)
            controller_4.channel_on(1)
        if command == 'clon':
            controller_4.channel_on(7)
        if command == 'cloff':
            controller_4.channel_off(7)
        if command == 'blon':
            controller_3.channel_on(7)
        if command == 'bloff':
            controller_3.channel_off(7)
        if command == 'lplon':
            controller_3.channel_on(6)
        if command == 'lploff':
            controller_3.channel_off(6)
        if command == 'ltlon':
            controller_3.channel_on(5)
        if command == 'ltloff':
            controller_3.channel_off(5)

        if command == 'hon':
            controller_3.channel_on(13)
        if command == 'hoff':
            controller_3.channel_off(13)
        if command == 'e':
            break
    #kitchen led stripe
    # i = 0x6
    # print("Out put id: {0}".format(i))
    # controller_4.channel_on(i)
    # command = input("Press something for the continue")
    # if command == 'n':
    #     controller_4.channel_off(i)
    #     time.sleep(3)

# On/Off test
#     print("Turn on 0x3")
#     controller_3.channel_on(0x1)
#     time.sleep(1)
#     controller_3.channel_on(0x2)
#     time.sleep(1)
#     controller_3.channel_on(0x3)
#     time.sleep(1)
#     controller_3.channel_on(0x4)
#     time.sleep(1)
#     controller_3.channel_on(0x5)
#     time.sleep(1)
#     controller_3.channel_on(0x6)
#     time.sleep(1)
#     controller_3.channel_on(0x7)
#     time.sleep(1)
#     controller_3.channel_on(0x8)
#     time.sleep(1)
#     controller_3.channel_on(0x9)
#     time.sleep(1)
#     controller_3.channel_on(0xA)
#     time.sleep(1)
#     controller_3.channel_on(0xB)
#     time.sleep(1)
#     controller_3.channel_on(0xC)
#     time.sleep(1)
#     controller_3.channel_on(0xD)
#     time.sleep(1)
#     controller_3.channel_on(0xE)
#     time.sleep(1)
#     controller_3.channel_on(0xF)
#     time.sleep(1)
#
#     print("Turn on 0x4")
#     controller_4.channel_on(0x1)
#     time.sleep(1)
#     controller_4.channel_on(0x2)
#     time.sleep(1)
#     controller_4.channel_on(0x3)
#     time.sleep(1)
#     controller_4.channel_on(0x4)
#     time.sleep(1)
#     controller_4.channel_on(0x5)
#     time.sleep(1)
#     controller_4.channel_on(0x6)
#     time.sleep(1)
#     controller_4.channel_on(0x7)
#     time.sleep(1)
#     controller_4.channel_on(0x8)
#     time.sleep(1)
#     controller_4.channel_on(0x9)
#     time.sleep(1)
#     controller_4.channel_on(0xA)
#     time.sleep(1)
#     controller_4.channel_on(0xB)
#     time.sleep(1)
#     controller_4.channel_on(0xC)
#     time.sleep(1)
#     controller_4.channel_on(0xD)
#     time.sleep(1)
#     controller_4.channel_on(0xE)
#     time.sleep(1)
#     controller_4.channel_on(0xF)
#     time.sleep(1)
#
#     print("Turn off 0x3")
#
#     controller_3.channel_off(0x1)
#     time.sleep(1)
#     controller_3.channel_off(0x2)
#     time.sleep(1)
#     controller_3.channel_off(0x3)
#     time.sleep(1)
#     controller_3.channel_off(0x4)
#     time.sleep(1)
#     controller_3.channel_off(0x5)
#     time.sleep(1)
#     controller_3.channel_off(0x6)
#     time.sleep(1)
#     controller_3.channel_off(0x7)
#     time.sleep(1)
#     controller_3.channel_off(0x8)
#     time.sleep(1)
#     controller_3.channel_off(0x9)
#     time.sleep(1)
#     controller_3.channel_off(0xA)
#     time.sleep(1)
#     controller_3.channel_off(0xB)
#     time.sleep(1)
#     controller_3.channel_off(0xC)
#     time.sleep(1)
#     controller_3.channel_off(0xD)
#     time.sleep(1)
#     controller_3.channel_off(0xE)
#     time.sleep(1)
#     controller_3.channel_off(0xF)
#     time.sleep(1)
#
#     print("Turn off 0x4")
#     controller_4.channel_off(0x1)
#     time.sleep(1)
#     controller_4.channel_off(0x2)
#     time.sleep(1)
#     controller_4.channel_off(0x3)
#     time.sleep(1)
#     controller_4.channel_off(0x4)
#     time.sleep(1)
#     controller_4.channel_off(0x5)
#     time.sleep(1)
#     controller_4.channel_off(0x6)
#     time.sleep(1)
#     controller_4.channel_off(0x7)
#     time.sleep(1)
#     controller_4.channel_off(0x8)
#     time.sleep(1)
#     controller_4.channel_off(0x9)
#     time.sleep(1)
#     controller_4.channel_off(0xA)
#     time.sleep(1)
#     controller_4.channel_off(0xB)
#     time.sleep(1)
#     controller_4.channel_off(0xC)
#     time.sleep(1)
#     controller_4.channel_off(0xD)
#     time.sleep(1)
#     controller_4.channel_off(0XE)
#     time.sleep(1)
#     controller_4.channel_off(0xF)
#     time.sleep(1)
#     controller_4.channel_off(0x10)
#     time.sleep(1)

if __name__ == "__main__":
    main()
