import socket
import time
from umodbus import conf
from umodbus.client.serial import rtu
from umodbus.utils import recv_exactly


class DOController:
    """Wrap basic Modbus operation with
    """

    def __init__(self, sock=None, slave_id=0x1):
        self.slave_id = slave_id
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('192.168.0.101', 20108))
        else:
            self.sock = sock

    def __del__(self):
        print("Close socket")
        self.sock.close()

    def send_msg(self, adu, sock):
        """ Send RTU ADU over socket to to server and return parsed response.

        :param adu: Request ADU.
        :param sock: Socket instance.
        :return: Parsed response from server.
        """
        sock.sendall(adu)

        # Check exception ADU (which is shorter than all other responses) first.
        exception_adu_size = 5
        response_error_adu = recv_exactly(sock.recv, exception_adu_size)
        rtu.raise_for_exception_adu(response_error_adu)

        expected_response_size = \
            rtu.expected_response_pdu_size_from_request_pdu(adu[1:-2]) + 3
        response_remainder = recv_exactly(
            sock.recv, expected_response_size - exception_adu_size)

        return rtu.parse_response_adu(response_error_adu + response_remainder, adu)

    def channel_on(self, channel):
        print("Turn On channel {}".format(channel))
        message = rtu.write_single_register(slave_id=self.slave_id, address=channel, value=0x0100)
        print(message)
        response = self.send_msg(message, self.sock)
        if response == 256:
            print("Success open rq")
        else:
            print("response {}".format(response))

    def channel_off(self, channel):
        print("Turn On channel {}".format(channel))
        message = rtu.write_single_register(slave_id=self.slave_id, address=channel, value=0x0200)
        print(message)
        response = self.send_msg(message, self.sock)
        if response == 512:
            print("Succes close rq")
        else:
            print("response {}".format(response))

    def get_channel_status(self, channel):
        print("Channel status {}".format(channel))
        message = rtu.read_holding_registers(slave_id=self.slave_id, starting_address=channel, quantity=0x0001)
        print(message)
        response = self.send_msg(message, self.sock)
        print("response {}".format(response))
        return response

    def get_slave_id(self):
        """slave_id=0xFF - broadcast messages"""
        message = rtu.read_holding_registers(slave_id=0xFF, starting_address=0xFF, quantity=0x0001)
        print(message)
        response = self.send_msg(message, self.sock)
        print("response {}".format(response))
        return response

    def set_slave_id(self, new_id):
        message = rtu.write_single_register(slave_id=self.slave_id, address=0xFF, value=new_id)
        print(message)
        response = self.send_msg(message, self.sock)
        print("response {}".format(response))
        return response


def main():
    controller_3 = DOController(slave_id=0x3)
    time.sleep(1)
    controller_4 = DOController(slave_id=0x4)
    time.sleep(1)
    # Can be used just with one connected unit
    # controller_3.get_slave_id()
    # time.sleep(1)
    # controller_4.get_slave_id()
    # controller.set_slave_id(new_id=0x0004)
    # controller.get_slave_id()

    print("Turn on 0x3")
    controller_3.channel_on(0x2)
    time.sleep(1)
    controller_3.channel_on(0x4)
    time.sleep(1)
    controller_3.channel_on(0x6)
    time.sleep(1)
    controller_3.channel_on(0x8)
    time.sleep(1)
    controller_3.channel_on(0xA)
    time.sleep(1)
    controller_3.channel_on(0xC)
    time.sleep(1)
    controller_3.channel_on(0xE)
    time.sleep(1)
    controller_3.channel_on(0x10)
    time.sleep(1)

    print("Turn on 0x4")
    controller_4.channel_on(0x1)
    time.sleep(1)
    controller_4.channel_on(0x2)
    time.sleep(1)
    controller_4.channel_on(0x3)
    time.sleep(1)
    controller_4.channel_on(0x4)
    time.sleep(1)
    controller_4.channel_on(0x5)
    time.sleep(1)
    controller_4.channel_on(0x6)
    time.sleep(1)
    controller_4.channel_on(0x7)
    time.sleep(1)
    controller_4.channel_on(0x8)
    time.sleep(1)
    controller_4.channel_on(0x9)
    time.sleep(1)
    controller_4.channel_on(0xA)
    time.sleep(1)
    controller_4.channel_on(0xB)
    time.sleep(1)
    controller_4.channel_on(0xC)
    time.sleep(1)
    controller_4.channel_on(0xD)
    time.sleep(1)
    controller_4.channel_on(0xE)
    time.sleep(1)
    controller_4.channel_on(0xF)
    time.sleep(1)
    controller_4.channel_on(0x01)
    time.sleep(1)

    print("Turn off 0x3")
    controller_3.channel_off(0x2)
    time.sleep(1)
    controller_3.channel_off(0x4)
    time.sleep(1)
    controller_3.channel_off(0x6)
    time.sleep(1)
    controller_3.channel_off(0x8)
    time.sleep(1)
    controller_3.channel_off(0xA)
    time.sleep(1)
    controller_3.channel_off(0xC)
    time.sleep(1)
    controller_3.channel_off(0XE)
    time.sleep(1)
    controller_3.channel_off(0x10)
    time.sleep(1)

    print("Turn off 0x4")
    controller_4.channel_off(0x1)
    time.sleep(1)
    controller_4.channel_off(0x2)
    time.sleep(1)
    controller_4.channel_off(0x3)
    time.sleep(1)
    controller_4.channel_off(0x4)
    time.sleep(1)
    controller_4.channel_off(0x5)
    time.sleep(1)
    controller_4.channel_off(0x6)
    time.sleep(1)
    controller_4.channel_off(0x7)
    time.sleep(1)
    controller_4.channel_off(0x8)
    time.sleep(1)
    controller_4.channel_off(0x9)
    time.sleep(1)
    controller_4.channel_off(0xA)
    time.sleep(1)
    controller_4.channel_off(0xB)
    time.sleep(1)
    controller_4.channel_off(0xC)
    time.sleep(1)
    controller_4.channel_off(0xD)
    time.sleep(1)
    controller_4.channel_off(0XE)
    time.sleep(1)
    controller_4.channel_off(0xF)
    time.sleep(1)
    controller_4.channel_off(0x10)
    time.sleep(1)

    # controller_4.channel_on(0xE)
    # print("Turn  0x4")
    # controller_4.channel_on(0xF)
    # print("Turn  0x4")
    # controller_4.channel_on(0x01)
    # time.sleep(1)
    # controller_3.channel_off(0xC)
    # print("Turn  0x4")
    # controller_3.channel_off(0XE)
    # print("Turn 0x4")
    # controller_3.channel_off(0x10)
    # time.sleep(1)

if __name__ == "__main__":
    main()