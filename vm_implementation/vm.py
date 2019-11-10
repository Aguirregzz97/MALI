from vm_implementation.operations import *  # pylint: disable=unused-wildcard-import

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


def run(input):
  quadruples = input['quadruples']
  set_input(input)

  while not end:
    quadruple = quadruples[q]
    operations[quadruple[0]](quadruple[1], quadruple[2], quadruple[3])
