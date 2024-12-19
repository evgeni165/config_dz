import xml.etree.ElementTree as ET


class Interpreter:
    def __init__(self, path_to_bin, limit):
        self.registers = [0] * limit
        self.code = 0
        try:
            with open(path_to_bin, 'rb') as file:
                self.code = int.from_bytes(file.read(), byteorder='little', signed=True)
        except FileNotFoundError:
            print('Файл не найден')

    def interpret(self):
        while self.code != 0:
            a = self.code & ((1 << 6) - 1)
            if a == 38:
                self.load_constant()
            elif a == 40:
                self.read_memory()
            elif a == 18:
                self.write_memory()
            elif a == 13:
                self.reverse()
            elif a == '_':
                self.code >>= 1
        self.dump_result()

    def dump_result(self):
        log_file = ET.ElementTree(ET.Element('tests'))

        for ind, val in enumerate(self.registers):
            if val > 2 ** 18 - 1:
                val ^= (1 << 19) - 1
                val = -val - 1

            test_el = ET.SubElement(log_file.getroot(), 'register')
            test_el.text = str(val)
            test_el.attrib['index'] = str(ind)

        log_file.write('C:/Users/Pro10/Desktop/result.xml')

    def load_constant(self):
        b = (self.code & ((1 << 13) - 1)) >> 6
        c = (self.code & ((1 << 36) - 1)) >> 13
        self.code >>= 48

        self.registers[b] = c

    def read_memory(self):
        b = (self.code & ((1 << 13) - 1)) >> 6
        c = (self.code & ((1 << 20) - 1)) >> 13
        d = (self.code & ((1 << 34) - 1)) >> 20
        self.code >>= 48

        self.registers[b] = self.registers[c + d]

    def write_memory(self):
        b = (self.code & ((1 << 13) - 1)) >> 6
        c = (self.code & ((1 << 33) - 1)) >> 13
        self.code >>= 48

        self.registers[c] = self.registers[b]

    def reverse(self):
        b = (self.code & ((1 << 13) - 1)) >> 6
        c = (self.code & ((1 << 33) - 1)) >> 13
        self.code >>= 48

        val = self.registers[c]
        val = bin(val)[2:]
        val = int(val[::-1], 2)

        self.registers[b] = val
