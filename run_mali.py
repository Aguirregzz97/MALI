# Run vm for MALI language.

from vm_implementation.vm import run
import sys
import os

if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please send a file.')
    raise SyntaxError('mali needs 1 file.')
  program_name = sys.argv[1]

  # TODO: Verificar extension del archivo

  # Read program.
  with open(program_name, 'r', newline='\n') as file:
    input = eval(file.read())

  try:
    run(input)
  except KeyboardInterrupt:
    print('Execution interrupted.')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
