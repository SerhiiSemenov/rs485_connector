import socket
import time
from umodbus import conf
from umodbus.client.serial import rtu
from umodbus.utils import recv_exactly


def send_msg(adu, sock):
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

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

print("Test num: {}".format(iter))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.101', 20108))

    # print("Open")
    # message = rtu.write_single_register(slave_id=0x1, address=0x2, value=0x0100)
    # print(message)
    # response = send_msg(message, sock)
    # print("response {}".format(response))
    # time.sleep(1)

    # print("Rq status")
    # message = rtu.read_holding_registers(slave_id=0x1, starting_address=0x2, quantity=0x0001)
    # print(message)
    # response = send_msg(message, sock)
    # print("response {}".format(response))
    # time.sleep(3)
    #
    # print("Close")
    # message = rtu.write_single_register(slave_id=0x1, address=0x2, value=0x0200)
    # print(message)
    # response = send_msg(message, sock)
    # print("response {}".format(response))
    # time.sleep(1)
    #
    # print("Rq status")
    # message = rtu.read_holding_registers(slave_id=0x1, starting_address=0x2, quantity=0x0001)
    # print(message)
    # response = send_msg(message, sock)
    # print("response {}".format(response))

print("Rq status")
message = rtu.read_holding_registers(slave_id=0x3, starting_address=0x0, quantity=0x0005)
print(message)
response = send_msg(message, sock)
print("response {}".format(response))

print("OFF")
message = rtu.write_single_register(slave_id=0x3, address=0x2, value=0x01)
print(message)
response = send_msg(message, sock)
print("response {}".format(response))
time.sleep(3)

print("OFF")
message = rtu.write_single_register(slave_id=0x3, address=0x2, value=0x02)
print(message)
response = send_msg(message, sock)
print("response {}".format(response))
time.sleep(1)

sock.close()