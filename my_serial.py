import time
import serial
import serial.tools.list_ports_windows
import threading
lock = threading.RLock()

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
    if my_serial is not None and my_serial.isOpen():
        data = package_head + [len(data)] + data + package_tail
        try:
            my_serial.write(bytes(data))
            print_data(data, True)
            return True
        except serial.serialutil.SerialTimeoutException:
            return False

def recv_data_package():
    if my_serial is not None and my_serial.isOpen():
        try:
            if (my_serial.read(2) != bytes(package_head)):
                return None
            result = list(my_serial.read(int.from_bytes(my_serial.read())))
            if (my_serial.read(2) != bytes(package_tail)):
                return None
            print_data(result, False)
        except serial.SerialTimeoutException:
            return None
        return result


def send_write_order(data):
    if my_serial is not None and my_serial.isOpen():
        with lock:
            send_data_queue.append(('w', data))

def send_read_order(data, recv_func):
    if my_serial is not None and my_serial.isOpen():
        with lock:
            send_data_queue.append(('r', data, recv_func))


connected = False
running = True
send_data_queue = []    # ('w'/'r'，数据本身，[读指令给一个函数接收返回值])
def serial_thread():
    global connected

    while not connected:
        time.sleep(5)
        connected = True
        # for i in iter_port():
        #     print(f'尝试连接 {i}', end=' ---- ')
        #     if open_serial(i):
        #         print('尝试握手', end=' ---- ')
        #         flag = True
        #         if not send_data_package([0x02, 0x00]):
        #             flag = False
        #         else:
        #             recv = recv_data_package()
        #             if recv is None or len(recv) != 1 or recv[0] != 0x66:
        #                 flag = False
        #         if flag:
        #             print('握手成功，成功连接到下位机')
        #             connected = True
        #             break
        #         else:
        #             print('握手失败，此连接不是下位机')
        #     else:
        #         print('连接失败')

    while running:
        if send_data_queue:
            with lock:
                data = send_data_queue.pop(0)
            if data[0] == 'w':
                send_data_package([0x12] + data[1])
                while int.from_bytes(my_serial.read()) != 0x88:
                    pass
            elif data[0] == 'r':
                if send_data_package([0x02] + data[1]):
                    recv = recv_data_package()
                    if recv is not None:
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
            timeout=1,
            write_timeout=1
            )
        my_serial.timeout = 1
    except serial.serialutil.SerialException:
        opened = False

    return opened

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

def start_connect():
    t = threading.Thread(target=serial_thread)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    print(iter_port())
    serial_thread()
