# Semantic checks and quadruple generation for MALI language.

from implementation.utils.semantic_and_quadruples_utils import *
from implementation.utils.generic_utils import *
from implementation.utils.constants import *
import re

# Semantic table filling.

classes = {'#global': new_class_dict(name='#global', parent=None)}

current_class = classes['#global']
current_function = current_class['#funcs']['#attributes']
current_access = None
current_type = None
is_param = False
current_x = None
current_y = None


def seen_class(class_name):
  if class_name in classes:
    return f"Repeated class name: {class_name}"
  else:
    global current_class, current_function
    classes[class_name] = new_class_dict(class_name)
    current_class = classes[class_name]
    current_function = current_class['#funcs']['#attributes']


def class_parent(class_parent):
  if class_parent not in classes:
    return f"Undeclared class parent: {class_parent}"
  else:
    current_class['#parent'] = class_parent


def finish_class():
  global current_class, current_function
  current_class = classes['#global']
  current_function = current_class['#funcs']['#attributes']
  current_access = '#public'


def seen_func(func_name):
  global func_size, current_function
  func_size = 0
  if func_name in current_class['#funcs']:
    return f"Redeclared function {func_name}"
  else:
    current_class['#funcs'][func_name] = new_func_dict(func_name, current_type)
    current_function = current_class['#funcs'][func_name]


def seen_access(new_access):
  global current_access
  current_access = new_access


def seen_type(new_type):
  if new_type not in func_types and (
        new_type not in classes):
    return f"{new_type} is not a class nor data type"
  else:
    global current_type
    current_type = new_type


def var_name(var_name):
  global param_count, var_count, current_access
  if var_name in current_function['#vars']:
    return f"Redeclared variable: {var_name}"
  else:
    if is_param:
      param_count += 1
    else:
      var_count += 1
    address = current_function['#var_avail'].next(current_type)
    adjust = 0
    if current_function['#name'] == '#attributes':
      adjust = INSTANCE_ADJUSTMENT
      if current_class['#name'] == '#global':
        adjust = GLOBAL_ADJUSTMENT

    current_function['#vars'][var_name] = (
          new_var_dict(current_type, address-adjust, current_access))


def set_param(params_ahead):
  global param_count, is_param
  if params_ahead:
    param_count = 0
  else:
    current_function['#param_count'] = param_count
  is_param = params_ahead


def set_access():
  current_function['#access'] = current_access


# Intermediate code generation.

operators = []
types = []
operands = []
quadruples = [[operations['goto'], None, None, None]]
visual_quadruples = [['goto', None, None, None]]
jumps = []
returns_count = 0
q_count = 1
const_avail = Available(CONSTANT_LOWER_LIMIT, CONSTANT_UPPER_LIMIT, const_types)
constant_addresses = {}
calling_class = None
calling_function = None
param_count = 0
var_count = 0


def address_or_else(operand, is_visual=False):
  if operand:
    if isinstance(operand, Operand):
      if is_visual:
        return operand.get_raw()
      else:
        return operand.get_address()
    else:
      return operand
  return None


def generate_quadruple(a, b, c, d):
  global q_count, quadruples, visual_quadruples

  operation = operations.get(a, f'NOT FOUND {a}')
  left_operand = address_or_else(b)
  right_operand = address_or_else(c)
  result = address_or_else(d)

  quadruples.append([operation, left_operand, right_operand, result])
  q_count += 1

  v_left_operand = address_or_else(b, True)
  v_right_operand = address_or_else(c, True)
  v_result = address_or_else(d, True)
  visual_quadruples.append([a, v_left_operand, v_right_operand, v_result])


def find_var_and_populate_operand(operand, prefix, mark_assigned,
                                      check_access=False):
  raw_operand = operand.get_raw()
  var = prefix.get(raw_operand, None)
  if not var:
    return False
  if mark_assigned:
    var['#assigned'] = True
  if not var['#assigned']:
    operand.set_error(f'Variable {raw_operand} used before assignment')
  elif check_access and var.get('#access', 'public') == 'private':
    operand.set_error(f'Variable {raw_operand} has private access')
  else:
    operand.set_type(var['#type'])
    operand.set_address(var['#address'])
    return True


def populate_non_constant_operand(operand, mark_assigned=False):
  # Search for var in function's local vars.
  function_vars = current_function['#vars']
  if find_var_and_populate_operand(operand, function_vars, mark_assigned):
    return
  # Search for var in the attributes from the class.
  class_attributes = current_class['#funcs']['#attributes']['#vars']
  if find_var_and_populate_operand(operand, class_attributes, mark_assigned):
    return
  # Search for var in the attributes of inherited classes.
  curr_class = current_class['#parent']
  while curr_class:
    class_attributes = classes[curr_class]['#funcs']['#attributes']['#vars']
    if find_var_and_populate_operand(operand, class_attributes, mark_assigned,
                                     True):
      return
    curr_class = classes[curr_class]['#parent']

  if not operand.get_error():
    operand.set_error(f'Variable {operand.get_raw()} not in scope.')


def get_or_create_cte_address(value, val_type):
  global constant_addresses
  if value in constant_addresses:
    return constant_addresses[value]
  else:
    address = const_avail.next(val_type)
    constant_addresses[value] = address
    return address


def build_operand(raw_operand):
  t = type(raw_operand)
  operand = Operand(raw_operand)
  if t == int:
    address = get_or_create_cte_address(raw_operand, 'int')
    operand.set_type('int')
    operand.set_address(address)
  elif t == float:
    address = get_or_create_cte_address(raw_operand, 'float')
    operand.set_type('float')
    operand.set_address(address)
  elif t == bool:
    address = get_or_create_cte_address(raw_operand, 'bool')
    operand.set_type('bool')
    operand.set_address(address)
  elif t == str:
    if re.match(r"\'.\'", raw_operand):
      address = get_or_create_cte_address(raw_operand, 'char')
      operand.set_type('char')
      operand.set_address(address)
    else:
      populate_non_constant_operand(operand)
  return operand


def register_operand(raw_operand):
  global operands, types
  operand = build_operand(raw_operand)
  if operand.get_error(): return operand.get_error()
  operands.append(operand)
  types.append(operand.get_type())


def register_operator(operator):
  global operators
  operators.append(str(operator))


def build_temp_operand(op_type):
  global current_function
  address = current_function['#temp_avail'].next(op_type)
  current_function['#vars'][address] = new_var_dict(op_type, address)
  current_function['#var_count'] += 1
  operand = Operand()
  operand.set_address(address)
  operand.set_type(op_type)
  return operand


def solve_operation_or_continue(ops):
  global operators, types, operands
  operator = top(operators)
  if operator in ops:
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    operator = operators.pop()
    result_type = semantic_cube[left_type][right_type][operator]
    if not result_type:
      return (f'Type mismatch: Invalid operation {operator} on given operands')
    temp = build_temp_operand(result_type)
    generate_quadruple(operator, left_operand, right_operand, temp)
    operands.append(temp)
    types.append(result_type)


def pop_fake_bottom():
  global operators
  operators.pop()


def do_assign(result):
  global operators, types, operands
  left_operand = operands.pop()
  left_type = types.pop()
  result_operand = Operand(result)
  populate_non_constant_operand(result_operand, True)
  if result_operand.get_error(): return result_operand.get_error()
  result_type = result_operand.get_type()
  if not semantic_cube[result_type][left_type]['=']:
    return (f'Type mismatch: expression cannot be assigned to {result}')
  generate_quadruple('=', left_operand, None, result_operand)
  types.append(result_type)


def do_write(s):
  if s:
    operand = Operand(s)
    operand.set_type('cte_string')
    operand.set_address(const_avail.next('cte_string'))
    generate_quadruple('write', None, None, operand)
  else:
    word = operands.pop()
    type = types.pop()
    operand = build_operand(word)
    if operand.get_error(): return operand.get_error()
    generate_quadruple('write', None, None, word)


def do_read():
  global operands, types
  operand = Operand('read')
  operand.set_address(operations['read'])
  operand.set_type('dynamic')
  operands.append(operand)
  types.append('dynamic')


def register_condition():
  exp_type = types.pop()
  if exp_type != 'bool':
    return 'Evaluated expression is not boolean'
  result = operands.pop()
  generate_quadruple('gotof', result, None, None)
  jumps.append(q_count-1)


def register_else():
  generate_quadruple('goto', None, None, None)
  false = jumps.pop()
  jumps.append(q_count-1)
  quadruples[false][3] = q_count


def register_end_if():
  end = jumps.pop()
  quadruples[end][3] = q_count


def register_while():
  jumps.append(q_count)


def register_end_while():
  end = jumps.pop()
  quadruples[end][3] = q_count
  ret = jumps.pop()
  generate_quadruple('goto', None, None, ret)


def end_vars():
  global var_count
  current_function['#var_count'] = var_count
  var_count = 0


def register_function_beginning():
  current_function['#start'] = q_count


def set_current_type_void():
  global current_type
  current_type = 'void'


def register_main_beginning():
  quadruples[0][3] = q_count
  visual_quadruples[0][3] = q_count


def register_func_end(is_main=False):
  global returns_count
  while returns_count:
    quadruples[jumps.pop()][3] = q_count
    returns_count -= 1
  if is_main:
    generate_quadruple('end', None, None, None)
  else:
    generate_quadruple('endproc', None, None, None)


def register_return():
  global returns_count
  function_type = current_function['#type']
  if function_type == 'void':
    return 'Void function cannot return a value'
  return_val = operands.pop()
  return_type = types.pop()
  if function_type != return_type:
    return f'Cannot return type {return_type} as {function_type}'
  generate_quadruple('return', return_val, None, None)
  jumps.append(q_count)
  returns_count += 1
  generate_quadruple('goto', None, None, None)


def call_parent(parent):
  global calling_class, calling_function
  if not current_class['#parent']:
    return (f"{current_class['#name']} has no parent class but tries "
        + f'to extend {parent} in constructor')
  elif parent != current_class['#parent']:
    return f"{parent} is not {current_class['#name']}'s parent"
  calling_class = classes[parent]
  calling_function = calling_class['#funcs']['init']


def seen_call(func_name):
  global calling_class, calling_function
  if func_name in current_class['#funcs']:
    calling_class = current_class
    calling_function = calling_class['#funcs'][func_name]
    return
  curr_class = current_class['#parent']
  while curr_class:
    if func_name in classes[curr_class]['#funcs']:
      calling_class = classes[curr_class]
      calling_function = calling_class['#funcs'][func_name]
      return
    curr_class = classes[curr_class]['#parent']
  return f"{func_name} not defined for {current_class['#name']}"


def start_param_collection():
  global param_count
  param_count = 0
  size = calling_function['#param_count'] + calling_function['#var_count']
  generate_quadruple('era', calling_function['#name'], None, None)


def pass_param():
  param = list(calling_function['#vars'].values())[param_count]
  param_type = param['#type']
  argument = operands.pop()
  arg_type = types.pop()
  if param_type != arg_type:
    return (f"{calling_function['#name']} expecting type {param_type} "
        + f'for parameter {param_count+1}')
  #TODO: en el ejemplo param se imprime el cuadruplo como 'param#'
  generate_quadruple('param', argument, None, param_count)


def prepare_upcoming_param():
  global param_count
  param_count += 1
  if param_count+1 > calling_function['#var_count']:
    expected = calling_function['#var_count']
    return (f'{calling_function} expects {expected} parameters, but more' +
        'were given')


def done_param_pass():
  expected = calling_function['#var_count']
  if param_count+1 != expected:
    return (f'{calling_function} expects {expected} parameters, but ' +
        f'{param_count+1} were given')
  generate_quadruple('gosub', calling_function['#name'], None,
                    calling_function['#start'])


def get_cleaned_symbol_table():
  for c in classes:
    if classes[c]['#parent'] == '#global':
      classes[c]['#parent'] = None
    for f in classes[c]['#funcs']:
      del classes[c]['#funcs'][f]['#var_avail']
      del classes[c]['#funcs'][f]['#temp_avail']

  constant_segment = invert_dict(constant_addresses)

  output = {
    'symbol_table': classes,
    'constant_segment': constant_segment,
    'quadruples': quadruples,
  }

  return output
