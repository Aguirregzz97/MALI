from implementation.parser import *
import sys

program_name = ''

if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please send a file.')
    raise SyntaxError('mali needs 1 file.')
  program_name = sys.argv[1]

  # TODO: Verificar extension del archivo

  # Compile program.
  with open(program_name, 'r', newline='\n') as file:
    parse_string(file.read())

  # Generate object code file.
  output = generate_output()
  if output:
    with open(program_name + 'r', 'w') as file:
      file.write(output)
