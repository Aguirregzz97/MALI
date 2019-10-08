import glob, os
from parser import *


if __name__ == '__main__':
    os.chdir('testfiles')
    for file_name in glob.glob('correctos/*_test.m'):
        file = open(file_name, 'r')
        try:
            parser.parse(file.read())
            print(f'Successfull {file_name}.')
        except SyntaxError:
            print(f'Fail        {file_name}.')
