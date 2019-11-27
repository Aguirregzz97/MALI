# Run compiler from MALI language.

from implementation.parser import *  # pylint: disable=unused-wildcard-import
import sys


if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please send a file.')
    raise SyntaxError('mali needs 1 file.')
  program_name = sys.argv[1]

  # Compile program.
  with open(program_name, 'r', newline='\n') as file:
    try:
      object_code = parse_and_generate_object_code(file.read())
      if object_code:
        with open(program_name + 'o', 'w') as file:
          file.write(object_code)
    except:
      pass
