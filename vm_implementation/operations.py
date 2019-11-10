from vm_implementation.memory import Memory  # pylint: disable=unused-wildcard-import

memory: Memory
symbol_table = None
q = 0
end = False


def set_input(input):
  global memory, symbol_table
  symbol_table = input['symbol_table']
  memory = Memory(symbol_table)
  for address, value in input['data_segment'].items():
    memory.set(address, value)
  for address, value in input['constant_segment'].items():
    memory.set(address, value)
  memory.new_procedure('#global', '#main')


def should_end():
  return end


def get_q():
  return q


def next_q():
  global q
  q += 1


def op_plus_unary(a, b, c):
  next_q()


def op_minus_unary(a, b, c):
  next_q()


def op_not(a, b, c):
  next_q()


def op_times(a, b, c):
  memory.set(c, memory.get(a) * memory.get(b))
  next_q()


def op_div(a, b, c):
  b_val = memory.get(b)
  if b_val == 0:
    return 'Division by 0.'
  memory.set(c, memory.get(a) / b_val)
  next_q()


def op_plus(a, b, c):
  memory.set(c, memory.get(a) + memory.get(b))
  next_q()


def op_minus(a, b, c):
  memory.set(c, memory.get(a) - memory.get(b))
  next_q()


def op_less_than(a, b, c):
  next_q()


def op_more_than(a, b, c):
  next_q()


def op_different(a, b, c):
  next_q()


def op_is_equal(a, b, c):
  next_q()


def op_less_equal(a, b, c):
  next_q()


def op_more_equal(a, b, c):
  next_q()


def op_or(a, b, c):
  next_q()


def op_and(a, b, c):
  next_q()


def op_equal(a, b, c):
  # TODO: Enum de operaciones
  if a == 'read':
    read = input()
    # TODO: validar tipo.
    memory.set(c, read)
  else:
    memory.set(c, memory.get(a))
  next_q()


def op_read(a, b, c):
  next_q()


def op_write(a, b, c):
  if type(c) == str:
    print(c)
  else:
    print(memory.get(c))
  next_q()


def op_goto(a, b, c):
  global q
  q = c


def op_gotof(a, b, c):
  next_q()


def op_gosub(a, b, c):
  next_q()


def op_param(a, b, c):
  next_q()


def op_era(a, b, c):
  next_q()


def op_return(a, b, c):
  next_q()


def op_endproc(a, b, c):
  next_q()


def op_end(a, b, c):
  global end
  end = True


def op_switch_instance(a, b, c):
  next_q()


def op_exit_instances(a, b, c):
  next_q()


def op_get_return(a, b, c):
  next_q()


def op_fake_bottom(a, b, c):
  next_q()
