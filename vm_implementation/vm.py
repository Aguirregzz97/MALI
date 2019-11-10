import sys
from operations import *

program_name = ''


operations = [
  None,
  op_plus_unary,
  op_minus_unary,
  op_not,
  op_times,
  op_div,
  op_plus,
  op_minus,
  op_less_than,
  op_more_than,
  op_different,
  op_is_equal,
  op_less_equal,
  op_more_equal,
  op_or,
  op_and,
  op_equal,
  op_read,
  op_write,
  op_goto,
  op_gotof,
  op_gosub,
  op_param,
  op_era,
  op_return,
  op_endproc,
  op_end,
  op_switch_instance,
  op_exit_instances,
  op_get_return,
  op_fake_bottom
]


if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please send a file.')
    raise SyntaxError('mali needs 1 file.')
  program_name = sys.argv[1]

  # Read program.
  with open(program_name, 'r', newline='\n') as file:
      input = eval(file.read())
  quadruples = input['quadruples']

  set_input(input)

  while not end:
    operations[q[0]](q[1], q[2], q[3])
