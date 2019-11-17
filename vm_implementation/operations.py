from vm_implementation.utils.memory import Memory  # pylint: disable=unused-wildcard-import


memory: Memory
symbol_table = None
q = 0
aux_q = []
end = False
params = None


def set_input(input):
  global memory, symbol_table
  symbol_table = input['symbol_table']
  memory = Memory(symbol_table)
  for address, value in input['data_segment'].items():
    memory.set(address, value)
  for address, value in input['constant_segment'].items():
    memory.set(address, value)
  memory.push_new_procedure()


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
  memory.set(c, memory.get(a) < memory.get(b))
  next_q()


def op_more_than(a, b, c):
  memory.set(c, memory.get(a) > memory.get(b))
  next_q()


def op_different(a, b, c):
  memory.set(c, memory.get(a) != memory.get(b))
  next_q()


def op_is_equal(a, b, c):
  memory.set(c, memory.get(a) == memory.get(b))
  next_q()


def op_less_equal(a, b, c):
  memory.set(c, memory.get(a) <= memory.get(b))
  next_q()


def op_more_equal(a, b, c):
  memory.set(c, memory.get(a) >= memory.get(b))
  next_q()


def op_or(a, b, c):
  memory.set(c, memory.get(a) or memory.get(b))
  next_q()


def op_and(a, b, c):
  memory.set(c, memory.get(a)
             and memory.get(b))
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


def op_write(a, b, c):
  if type(c) == str:
    print(c, end='')
  else:
    elem = memory.get(c)
    if elem == '$':
      print()
    else:
      print(elem, end='')
  next_q()


def op_goto(a, b, c):
  global q
  q = c


def op_gotof(a, b, c):
  global q
  if not memory.get(a):
    q = c
  else:
    next_q()


def op_gosub(a, b, c):
  global q, aux_q
  aux_q.append(q + 1)
  q = symbol_table[a]['#funcs'][b]['#start']
  memory.push_new_procedure()


def op_param(a, b, c):
  address = params[c]['#address']
  memory.set(address, memory.get(a, assigning_param=True), assigning_param=True)
  next_q()


def op_era(a, b, c):
  global params
  memory.prepare_new_procedure(a, b)
  params = list(symbol_table[a]['#funcs'][b]['#vars'].values())
  next_q()


def op_return(a, b, c):
  global q
  memory.set_return(memory.get(a))
  q = c


def op_endproc(a, b, c):
  global q, aux_q
  memory.pop_procedure()
  q = aux_q.pop()


def op_end(a, b, c):
  # memory.print_memory()
  global end
  end = True


def op_enter_instance(a, b, c):
  memory.push_instance(a, c)
  next_q()


def op_exit_instance(a, b, c):
  memory.pop_instance()
  next_q()


def op_get_return(a, b, c):
  return_value = memory.get_return()
  if return_value is None:
    return 'Segmentation fault: missing return.'
  memory.set(c, return_value)
  next_q()

def op_ver(a, b, c):
  if not memory.get(b) <= memory.get(a) < memory.get(c):
    print(memory.get(a))
    return 'Index out of range'
  next_q()
