from vm_implementation.operations import *  # pylint: disable=unused-wildcard-import

program_name = ''

operations = [
    None,
    op_plus_unary,  # 1
    op_minus_unary,  # 2
    op_not,  # 3
    op_times,  # 4
    op_div,  # 5
    op_plus,  # 6
    op_minus,  # 7
    op_less_than,  # 8
    op_more_than,  # 9
    op_different,  # 10
    op_is_equal,  # 11
    op_less_equal,  # 12
    op_more_equal,  # 13
    op_or,  # 14
    op_and,  # 15
    op_equal,  # 16
    None,  # 17 (funcion read)
    op_write,  # 18
    op_goto,  # 19
    op_gotof,  # 20
    op_gosub,  # 21
    op_param,  # 22
    op_era,  # 23
    op_return,  # 24
    op_endproc,  # 25
    op_end,  # 26
    op_enter_instance,  # 27
    op_exit_instance,  # 28
    op_get_return,  # 29
    None,  # 30 (fake bottom)
    op_ver, # 31
]


def run(input):
  quadruples = input['quadruples']
  set_input(input)

  cont = 100
  while not should_end():
    quadruple = quadruples[get_q()]
    # print(get_q(), '-', operations[quadruple[0]].__name__, quadruple)
    e = operations[quadruple[0]](quadruple[1], quadruple[2], quadruple[3])
    if e:
      print(e)
      break
    cont -= 1
