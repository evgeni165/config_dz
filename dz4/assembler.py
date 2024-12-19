import xml.etree.ElementTree as ET


class Assembler:
    def __init__(self, path_to_code, path_to_log):
        self.path_to_log = path_to_log
        self.logs = []
        self.commands = []
        try:
            with open(path_to_code, 'rt') as file:
                self.commands = file.readlines()
        except FileNotFoundError:
            print('Файл не найден')
        except:
            print('Ошибка работы с файлом')

    def assemble(self, path_to_bin):
        with open(path_to_bin, 'wb') as file:
            for command in self.commands:
                if command.strip().startswith('#'):
                    continue

                try:
                    name, body = command.split(' ', 1)
                except ValueError:
                    continue

                body = tuple(map(int, body.split()))
                number = None
                bits = None
                if name == 'CONST':
                    number = 38
                    bits = Assembler.load_constant(*body)
                elif name == 'READ':
                    number = 40
                    bits = Assembler.read_memory(*body)
                elif name == 'WRITE':
                    number = 18
                    bits = Assembler.write_memory(*body)
                elif name == 'REVERSE':
                    number = 13
                    bits = Assembler.reverse(*body)
                file.write(bits)
                self.logs.append([number, body, bits])
        self.make_log()

    def make_log(self):
        log_file = ET.ElementTree(ET.Element('tests'))

        for log in self.logs:
            test_el = ET.SubElement(log_file.getroot(), 'test')
            test_el.text = ' '.join(hex(i) for i in log[-1])
            for name, param in zip('ABCD', [log[0], *log[1]]):
                test_el.attrib[name] = str(param)

        log_file.write(self.path_to_log)

    @staticmethod
    def load_constant(b, c):
        bits = (c << 13) | (b << 6) | 38
        return bits.to_bytes(6, byteorder='little', signed=True)

    @staticmethod
    def read_memory(b, c, d):
        bits = (d << 20) | (c << 13) | (b << 6) | 40
        return bits.to_bytes(6, byteorder='little', signed=True)

    @staticmethod
    def write_memory(b, c):
        bits = (c << 13) | (b << 6) | 18
        return bits.to_bytes(6, byteorder='little', signed=True)

    @staticmethod
    def reverse(b, c):
        bits = (c << 13) | (b << 6) | 13
        return bits.to_bytes(6, byteorder='little', signed=True)
