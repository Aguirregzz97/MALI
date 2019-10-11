from implementation.parser import *
import sys

program_name = ''

if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please send a file.')
    raise SyntaxError('mali needs 1 file.')
  program_name = sys.argv[1]
  file = open(program_name, 'r', newline='\n')
  parseString(file.read())
  file.close()

