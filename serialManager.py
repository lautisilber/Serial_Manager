from time import sleep
from serial import Serial
from threading import Thread

class SerialCom(Thread):
    def __init__(self, end_char='$', delim_char='|', serial_port='/dev/ttyS0', baud_rate=115200, between_time=0.05):
        self.terminate = False
        self.end_char = end_char
        self.delim_char = delim_char
        self.in_buffer = ''
        self.between_time = between_time
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = Serial(self.serial_port, self.baud_rate)
        Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            try:
                while self.ser.in_waiting:
                    in_byte = self.ser.read().decode('utf-8')
                    if in_byte == self.end_char:
                        self.callback()
                        self.in_buffer = ''
                    elif not (32 <= ord(in_byte) <= 126 or in_byte == '\n'):
                        pass
                    else:
                        self.in_buffer += in_byte
            except:
                pass

    def send_msg(self, msg: str):
        if not msg.endswith(self.end_char):
            msg += self.end_char
        self.ser.write(bytes(msg, 'utf-8'))

    def split_msg(self, custom_str=None, delim=None):
        string = self.in_buffer if custom_str is None else custom_str
        delim = ' ' if delim is None else delim
        index = string.find(delim)
        if index == -1:
            return string, ''
        head = string[:index]
        body = ''
        if index < len(string)-1:
            body = string[index+1:]
        return head, body

    def callback(self):
        head, body = self.split_msg()
        print(f'head: "{head}"\nbody:"{body}"')
        

def get_serial():
    ser = SerialCom()
    ser.start()
    return ser
