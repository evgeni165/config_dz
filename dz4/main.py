from sys import argv
from os.path import exists
from assembler import Assembler
from interpreter import Interpreter


def assemble():
    if len(argv) < 5:
        print('Введены не все аргументы для корректной работы ассемблера')
        return
    path_to_code = argv[2]
    path_to_bin = argv[3]
    path_to_log = argv[4]

    if not exists(path_to_code):
        print('Файла с таким именем не существует')
        return

    my_assembler = Assembler(path_to_code, path_to_log)
    my_assembler.assemble(path_to_bin)


def interpret():
    if len(argv) < 4:
        print('Введены не все аргументы для корректной работы ассемблера')
        return

    path_to_bin = argv[2]
    limitation = argv[3]

    if not exists(path_to_bin):
        print('Файла с таким именем не существует')
        return

    try:
        limitation = int(limitation)
    except ValueError:
        print('Ограничение должно быть задано целым числом')
        return

    my_interpreter = Interpreter(path_to_bin, limitation)
    my_interpreter.interpret()


if __name__ == '__main__':
    if len(argv) < 2:
        print('Не введено имя подпрограммы для исполнения')
    if argv[1] == 'assemble':
        assemble()
    elif argv[1] == 'interpret':
        interpret()
