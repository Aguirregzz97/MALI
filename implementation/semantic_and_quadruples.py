# Semantic checks and quadruple generation for MALI language.

from implementation.utils.semantic_and_quadruples_utils import *  # pylint: disable=unused-wildcard-import
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
param_count = 0
var_count = 0
var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT, var_types)
temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT, temp_types)


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
  global current_class, current_function, current_access
  current_class = classes['#global']
  current_function = current_class['#funcs']['#attributes']
  current_access = '#public'


def seen_func(func_name):
  global func_size, current_class, current_function, var_avail, temp_avail
  func_size = 0
  if func_name in current_class['#funcs']:
    return f"Redeclared function {func_name}"
  else:
    current_class['#funcs'][func_name] = new_func_dict(func_name, current_type)
    current_function = current_class['#funcs'][func_name]
  var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT, var_types)
  temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT, temp_types)


def seen_access(new_access):
  global current_access
  current_access = new_access


def seen_type(new_type):
  global current_type
  if new_type not in func_types and (
          new_type not in classes):
    return f"{new_type} is not a class nor data type"
  current_type = new_type


def var_name(var_name):
  global param_count, var_count
  if var_name in current_function['#vars']:
    return f"Redeclared variable: {var_name}"
  else:
    if is_param:
      param_count += 1
    else:
      var_count += 1
    address = var_avail.next(current_type)
    if not address:
      return 'Too many variables.'
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
quadruples = [[Operations.GOTO.value, None, None, None]]
visual_quadruples = [[Operations.GOTO, None, None, None]]
jumps = []
returns_count = 0
q_count = 1
const_avail = Available(CONSTANT_LOWER_LIMIT, CONSTANT_UPPER_LIMIT,
                        const_types)
constant_addresses = {}
calling_class = None
calling_function = None
aux_current_class = None
aux_current_function = None
called_attribute = None


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

  left_operand = address_or_else(b)
  right_operand = address_or_else(c)
  result = address_or_else(d)

  quadruples.append([a.value, left_operand, right_operand, result])
  q_count += 1

  v_left_operand = address_or_else(b, True)
  v_right_operand = address_or_else(c, True)
  v_result = address_or_else(d, True)
  visual_quadruples.append([a.name, v_left_operand, v_right_operand, v_result])


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


def populate_aux(class_prefix, function_prefix, operand, mark_assigned=False):
  # Search for var in function's local vars.
  function_vars = function_prefix['#vars']
  if find_var_and_populate_operand(operand, function_vars, False):
    return
  # Search for var in the attributes from the class.
  class_attributes = class_prefix['#funcs']['#attributes']['#vars']
  if find_var_and_populate_operand(operand, class_attributes, False):
    return
  # Search for var in the attributes of inherited classes.
  curr_class = class_prefix['#parent']
  while curr_class:
    class_attributes = classes[curr_class]['#funcs']['#attributes']['#vars']
    if find_var_and_populate_operand(operand, class_attributes, False, True):
      return
    curr_class = classes[curr_class]['#parent']

  if not operand.get_error():
    operand.set_error(f'Variable {operand.get_raw()} not in scope.')


def populate_attribute(operand):
  populate_aux(calling_class, calling_function, operand)


def populate_non_constant_operand(operand, mark_assigned=False):
  populate_aux(current_class, current_function, operand, mark_assigned)


def get_or_create_cte_address(value, val_type):
  global constant_addresses
  if value in constant_addresses:
    return constant_addresses[value]
  else:
    address = const_avail.next(val_type)
    constant_addresses[value] = address
    return address


def find_and_build_operand(raw_operand):
  t = type(raw_operand)
  operand = Operand(raw_operand)
  if t == int:
    address = get_or_create_cte_address(raw_operand, Types.INT)
    if not address:
      operand.set_error('Too many int constants.')
    operand.set_type(Types.INT)
    operand.set_address(address)
  elif t == float:
    address = get_or_create_cte_address(raw_operand, Types.FLOAT)
    if not address:
      operand.set_error('Too many float constants.')
    operand.set_type(Types.FLOAT)
    operand.set_address(address)
  # TODO: This might not occur.
  elif t == bool:
    address = get_or_create_cte_address(raw_operand, Types.BOOL)
    if not address:
      operand.set_error('Too many bool constants.')
    operand.set_type(Types.BOOL)
    operand.set_address(address)
  elif t == str:
    if re.match(r"\'.\'", raw_operand):
      address = get_or_create_cte_address(raw_operand, Types.CHAR)
      if not address:
        operand.set_error('Too many char constants.')
      operand.set_type(Types.CHAR)
      operand.set_address(address)
    else:
      populate_non_constant_operand(operand)
      if not operand.get_address():
        operand.set_error('Too many variables.')
  return operand


def register_operand(raw_operand):
  global operands, types
  operand = find_and_build_operand(raw_operand)
  if operand.get_error():
    return operand.get_error()
  operands.append(operand)
  types.append(operand.get_type())


def register_operator(operator):
  global operators
  operators.append(operator)


def build_temp_operand(op_type):
  global current_function
  operand = Operand()
  address = temp_avail.next(op_type)
  if not address:
    operand.set_error('Too many variables.')
  current_function['#vars'][address] = new_var_dict(op_type, address)
  current_function['#var_count'] += 1
  operand.set_address(address)
  operand.set_type(op_type)
  return operand


def solve_operation_or_continue(ops):
  global operators, operands, types
  operator = top(operators)
  if operator in ops:
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    operator = operators.pop()
    result_type = semantic_cube[left_type][right_type][operator]
    if not result_type:
      if left_type == Types.VOID or right_type == Types.VOID:
        return f'Expression returns no value.'
      return (f'Type mismatch: Invalid operation {operator} on given operands')
    temp = build_temp_operand(result_type)
    if temp.get_error():
      return temp.get_error()
    generate_quadruple(operator, left_operand, right_operand, temp)
    operands.append(temp)
    types.append(result_type)


def pop_fake_bottom():
  global operators
  operators.pop()


def do_assign(result):
  global operators, operands, types
  left_operand = operands.pop()
  left_type = types.pop()
  result_operand = Operand(result)
  populate_non_constant_operand(result_operand, True)
  if result_operand.get_error():
    return result_operand.get_error()
  result_type = result_operand.get_type()
  if not semantic_cube[result_type][left_type][Operations.EQUAL]:
    if left_type == Types.VOID:
      return f'Expression returns no value.'
    return (f'Type mismatch: expression cannot be assigned to {result}')
  generate_quadruple(Operations.EQUAL, left_operand, None, result_operand)
  types.append(result_type)


def do_write(s):
  global operands, types
  if s:
    operand = Operand(s)
    operand.set_type(Types.CTE_STRING)
    operand.set_address(const_avail.next(Types.CTE_STRING))
  else:
    operand = operands.pop()
    types.pop()
  generate_quadruple(Operations.WRITE, None, None, operand)


def do_read():
  global operands, types
  operand = Operand('read')
  operand.set_address(Operations.READ.value)
  operand.set_type(Types.READ)
  operands.append(operand)
  types.append(Types.READ)


def register_condition():
  global operands, types
  exp_type = types.pop()
  if exp_type != Types.BOOL:
    return 'Evaluated expression is not boolean'
  result = operands.pop()
  generate_quadruple(Operations.GOTOF, result, None, None)
  jumps.append(q_count-1)


def register_else():
  generate_quadruple(Operations.GOTO, None, None, None)
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
  generate_quadruple(Operations.GOTO, None, None, ret)


def end_vars():
  global var_count
  current_function['#var_count'] = var_count
  var_count = 0


def register_function_beginning():
  current_function['#start'] = q_count


def set_current_type_void():
  global current_type
  current_type = Types.VOID


def register_main_beginning():
  quadruples[0][3] = q_count
  visual_quadruples[0][3] = q_count


def register_func_end(is_main=False):
  global returns_count
  if current_function['#type'] != Types.VOID and returns_count == 0:
    return f"No return statement on non-void function {current_function['#name']}"
  while returns_count:
    quadruples[jumps.pop()][3] = q_count
    returns_count -= 1
  if is_main:
    generate_quadruple(Operations.END, None, None, None)
  else:
    generate_quadruple(Operations.ENDPROC, None, None, None)


def register_return():
  global returns_count, operands, types
  function_type = current_function['#type']
  if function_type == Types.VOID:
    return 'Void function cannot return a value'
  return_val = operands.pop()
  return_type = types.pop()
  if not semantic_cube[function_type][return_type][Operations.EQUAL]:
    return f'Cannot return type {return_type} as {function_type}'
  generate_quadruple(Operations.RETURN, return_val, None, None)
  jumps.append(q_count)
  returns_count += 1
  generate_quadruple(Operations.GOTO, None, None, None)


def call_parent(parent):
  global calling_class, calling_function
  if not current_class['#parent']:
    return (f"{current_class['#name']} has no parent class but tries "
            + f'to extend {parent} in constructor')
  elif parent != current_class['#parent']:
    return f"{parent} is not {current_class['#name']}'s parent"
  calling_class = classes[parent]
  calling_function = calling_class['#funcs']['init']


def finish_parent_call():
  global calling_class, calling_function, operands, types
  calling_class = current_class
  calling_function = current_function
  operands.append(Types.VOID)
  types.append(Types.VOID)


def start_func_call(func_name):
  global calling_class, calling_function
  if func_name in calling_class['#funcs']:
    calling_function = calling_class['#funcs'][func_name]
    return
  curr_class = calling_class['#parent']
  while curr_class:
    if func_name in classes[curr_class]['#funcs']:
      calling_class = classes[curr_class]
      calling_function = calling_class['#funcs'][func_name]
      return
    curr_class = classes[curr_class]['#parent']
  return f"{func_name} not defined in scope."


def start_param_collection():
  global param_count
  param_count = 0
  size = calling_function['#param_count'] + calling_function['#var_count']
  generate_quadruple(
      Operations.ERA, calling_class['#name'], calling_function['#name'], size)


def pass_param():
  global operands, types
  param = list(calling_function['#vars'].values())[param_count]
  param_type = param['#type']
  argument = operands.pop()
  arg_type = types.pop()
  if param_type != arg_type:
    return (f"{calling_function['#name']} expecting type {param_type} "
            + f'for parameter {param_count+1}')
  # TODO: en el ejemplo param se imprime el cuadruplo como 'param#'
  generate_quadruple(Operations.PARAM, argument, None, param_count)


def prepare_upcoming_param():
  global param_count
  param_count += 1
  expected = calling_function['#param_count']
  if param_count+1 > expected:
    return (f"{calling_function['#name']} expects {expected} parameters, " +
            'but more were given')


def done_param_pass():
  expected = calling_function['#param_count']
  if param_count+1 != expected and not param_count == 0 and not expected == 0:
    return (f"{calling_function['#name']} expects {expected} parameters, " +
            f'but {param_count+1} were given')
  generate_quadruple(
      Operations.GOSUB, calling_class['#name'], calling_function['#name'], None)


def attribute_call(attribute):
  global calling_function, called_attribute
  calling_function = calling_class['#funcs']['#attributes']
  called_attribute = Operand(attribute)
  populate_attribute(called_attribute)
  if called_attribute.get_error():
    return called_attribute.get_error()
  generate_quadruple(Operations.RETURN, called_attribute, None, None)


def finish_call():
  global calling_class, calling_function, operands, types

  generate_quadruple(Operations.EXIT_INSTANCES, None, None, None)

  if calling_function['#name'] == '#attributes':
    op_type = called_attribute.get_type()
  else:
    op_type = calling_function['#type']

  if op_type == Types.VOID:
    operands.append(Types.VOID)
    types.append(Types.VOID)
  else:
    operand = build_temp_operand(op_type)
    operand.set_raw(operand.get_address())
    generate_quadruple(Operations.GET_RETURN, None, None,
                       operand.get_address())
    operands.append(operand)
    types.append(operand.get_type())

  calling_class = current_class
  calling_function = current_function


def switch_func(func_name):
  global calling_function
  calling_function = calling_class['#funcs'][func_name]


def switch_instance(instance):
  global calling_class, calling_function

  calling_function = current_function

  operand = Operand(instance)
  populate_attribute(operand)
  class_type = operand.get_type()
  if operand.get_error():
    return operand.get_error()
  elif class_type in var_types:
    return f'{instance} is of type {class_type} and not an instance.'
  generate_quadruple(Operations.SWITCH_INSTANCE, operand, None, None)

  calling_class = classes[class_type]


def generate_output():
  global classes
  data_segment = (
      {v['#address']: None for v in
          classes['#global']['#funcs']['#attributes']['#vars'].values()})
  constant_segment = invert_dict(constant_addresses)

  # Clean symbol table for use in virtual machine.
  for v1 in classes.values():
    if v1['#parent'] == '#global':
      v1['#parent'] = None
    for v2 in v1['#funcs'].values():
      v2['#type'] = v2['#type'].value
      if '#access' in v2:
        del v2['#access']
      for v3 in v2['#vars'].values():
        del v3['#assigned']
        if type(v3['#type']) != str:
          v3['#type'] = v3['#type'].value
        if '#access' in v3:
          del v3['#access']

  del classes['#global']['#funcs']['#attributes']

  return {
      'symbol_table': classes,
      'data_segment': data_segment,
      'constant_segment': constant_segment,
      'quadruples': quadruples
  }
