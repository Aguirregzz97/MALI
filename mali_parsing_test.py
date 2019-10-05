import glob, os
from parser import parser


if __name__ == '__main__':
    os.chdir('tests')
    for file_name in glob.glob('*_test.m'):
        file = open(file_name, 'r')
        try:
            parser.parse(file.read())
        except SyntaxError:
            print(f'Error in file {file_name}.')
