from parser import *
import sys

program_name = 'test'

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Please send a file.')
        raise SyntaxError('mali needs 1 file.')
    program_name = sys.argv[1]
    file = open(program_name, 'r')
    parser.parse(file.read())
