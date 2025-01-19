import time
import serial
import serial.tools.list_ports_windows
import threading


def iter_port():
    return [i.name for i in serial.tools.list_ports_windows.iterate_comports()]


package_head = [0xff, 0xaa]
package_tail = [0x55, 0x00]

def print_data(data, from_me):
    global text_num
    if from_me:
        print(f'>>> [{', '.join((str(hex(i)) for i in data))}]')
    else:
        print(f'<<< [{', '.join((str(hex(i)) for i in data))}]')


def send_data_package(data):
    data = package_head + [len(data)] + data + package_tail
    print_data(data, True)
    my_serial.write(bytes(data))

def recv_data_package():
    if (my_serial.read(2) != bytes(package_head)):
        return None
    result = list(my_serial.read(int.from_bytes(my_serial.read())))
    if (my_serial.read(2) != bytes(package_tail)):
        return None
    print_data(result, False)
    return result


def send_write_order(data):
    send_data_queue.append(('w', data))

def send_read_order(data, recv_func):
    send_data_queue.append(('r', data, recv_func))


running = True
send_data_queue = []    # ('w'/'r'，数据本身，[读指令给一个函数接收返回值])
def serial_thread():
    while running:
        if send_data_queue:
            data = send_data_queue.pop(0)
            if data[0] == 'w':
                send_data_package([0x12] + data[1])
                while int.from_bytes(my_serial.read()) != 0x88:
                    pass
            elif data[0] == 'r':
                send_data_package([0x02] + data[1])
                recv = recv_data_package()
                data[2](recv)
        else:
            time.sleep(0.1)

my_serial = None

def open_serial(com):
    global my_serial

    opened = True

    try:
        my_serial = serial.Serial(
            port=com,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            )
    except serial.serialutil.SerialException:
        opened = False

    if opened:
        print("打开串口成功")
        print(my_serial.name)
        t = threading.Thread(target=serial_thread)
        t.daemon = True
        t.start()
    else:
        print("打开串口失败")
open_serial('COM6')

def close_serial():
    global running
    running = False
    if my_serial is not None and my_serial.isOpen():
        my_serial.close()
        if my_serial.isOpen():
            print("串口未关闭")
        else:
            print("串口已关闭")
    else:
        print('串口未打开')


if __name__ == '__main__':
    print(iter_port())
