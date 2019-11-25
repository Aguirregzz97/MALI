# Operations run by the MALI language VM.

from vm_implementation.memory import MemoryManager, Error  # pylint: disable=unused-wildcard-import
from vm_implementation.utils.constants import *  # pylint: disable=unused-wildcard-import

memory: MemoryManager
symbol_table = None
q = 0
aux_q = []
end = False


def set_input(input):
  '''Grab data from the object code file.'''
  global memory, symbol_table
  symbol_table = input['symbol_table']
  memory = MemoryManager()
  # for address, value in input['data'].items():
  #   memory.set(address, value)
  for address, value in input['constants'].items():
    memory.set(address, value)
  memory.push_new_procedure()


def should_end():
  '''Access method for end.'''
  return end


def get_q():
  '''Access method for quadruple position.'''
  return q


def next_q():
  '''Increase quadruple position counter.'''
  global q
  q += 1


def op_plus_unary(op_address: int, n: None, result_address: int):
  memory.set(result_address, + memory.get(op_address))
  next_q()


def op_minus_unary(op_address: int, n: None, result_address: int):
  memory.set(result_address, - memory.get(op_address))
  next_q()


def op_not(op_address: int, n: None, result_address: int):
  memory.set(result_address, int(not memory.get(op_address)))
  next_q()


def op_times(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform multiplication.'''
  memory.set(result_address,
             memory.get(l_op_address) * memory.get(r_op_address))
  next_q()


def op_div(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform division. Marks error if div by 0.'''
  b_val = memory.get(r_op_address)
  if b_val == 0:
    Error('Division by 0.')
  memory.set(result_address, memory.get(l_op_address) / b_val)
  next_q()


def op_plus(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform addition.'''
  memory.set(result_address,
             memory.get(l_op_address) + memory.get(r_op_address))
  next_q()


def op_minus(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform substraction.'''
  memory.set(result_address,
             memory.get(l_op_address) - memory.get(r_op_address))
  next_q()


def op_less_than(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform less than comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) < memory.get(r_op_address))
  next_q()


def op_more_than(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform more than comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) > memory.get(r_op_address))
  next_q()


def op_different(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform different than comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) != memory.get(r_op_address))
  next_q()


def op_is_equal(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform is equal to comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) == memory.get(r_op_address))
  next_q()


def op_less_equal(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform less equal to comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) <= memory.get(r_op_address))
  next_q()


def op_more_equal(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform more equal to comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) >= memory.get(r_op_address))
  next_q()


def op_or(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform or comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) or memory.get(r_op_address))
  next_q()


def op_and(l_op_address: int, r_op_address: int, result_address: int):
  '''Perform and comparison.'''
  memory.set(result_address,
             memory.get(l_op_address) and memory.get(r_op_address))
  next_q()


def op_equal(l_op, n: None, result_address: int):
  '''Perform assignment. Either from user input or operand.'''
  if l_op == '#read':
    read = input()
    memory.set(result_address, read)
  else:
    memory.set(result_address, memory.get(l_op))
  next_q()


def op_write(n1: None, n2: None, op):
  '''Perform console print. Either operand or str.'''
  if type(op) == str:
    print(op, end='')
  else:
    elem = memory.get(op, printable=True)
    print(elem, end='')
  next_q()


def op_goto(n1: None, n2: None, position: int):
  '''Perform goto.'''
  global q
  q = position


def op_gotof(op_address: int, n: None, position: int):
  '''Perform goto if given op is false.'''
  global q
  if not memory.get(op_address):
    q = position
  else:
    next_q()


def op_gosub(class_name: str, func_name: str, n: None):
  '''Change context to function.'''
  global q, aux_q
  aux_q.append(q + 1)
  q = symbol_table[class_name]['#funcs'][func_name]['#start']
  memory.push_new_procedure()


def op_param(op_address: int, n: None, param_address: int):
  '''Perform parameter pass to upcoming function.'''
  if op_address == '#read':
    read = input()
    memory.set(param_address, read, assigning_param=True)
  else:
    memory.set(param_address, memory.get(op_address), assigning_param=True)
  next_q()


def op_era(class_name: str, func_name: str, n: None):
  '''Create activation registry for given function.'''
  memory.prepare_new_procedure(class_name, func_name)
  next_q()


def op_return(op_address: int, n1: None, endproc_position: int):
  '''Perform return on function.'''
  global q
  memory.set_return(memory.get(op_address))
  q = endproc_position


def op_endproc(n1: None, n2: None, n3: None):
  '''Perform endproc.'''
  global q, aux_q
  memory.pop_procedure()
  q = aux_q.pop()


def op_end(n1: None, n2: None, n3: None):
  '''Perform execution end.'''
  global end
  end = True


def op_enter_instance(instnace_address: int, b, class_type: str):
  '''Change context to given instance.'''
  memory.push_instance(instnace_address, class_type)
  next_q()


def op_exit_instance(n1: None, n2: None, n3: None):
  '''Pop current instance.'''
  memory.pop_instance()
  next_q()


def op_get_return(result_address, n1: None, n2: None):
  '''Grab return value.'''
  memory.set(result_address, memory.get_return())
  next_q()


def op_ver(op_address, lower_limit, upper_limit):
  '''Verify that index is within accepted bounds.'''
  if not lower_limit <= memory.get(op_address) <= upper_limit:
    Error('Index out of bounds.')
  next_q()


def op_set_foreign(n1: None, n2: None, n3: None):
  memory.setting_param = True
  next_q()


def op_unset_foreign(n1: None, n2: None, n3: None):
  memory.setting_param = False
  next_q()
