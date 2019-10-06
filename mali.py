# TODO: solo importar parser
from parser import *
import sys

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Please send a file.')
        raise SyntaxError('mali needs 1 file.')
    file = open(sys.argv[1], 'r')
    parser.parse(file.read())
    pp.pprint(classes)


