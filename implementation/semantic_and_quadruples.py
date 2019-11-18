# Semantic checks and quadruple generation for MALI language.

from implementation.utils.semantic_and_quadruples_utils import *  # pylint: disable=unused-wildcard-import
from implementation.utils.generic_utils import *
from implementation.utils.constants import *
import re

# Semantic table filling.

classes = {'#global': new_class_dict(name='#global', parent=None)}

current_class = classes['#global']
current_function = current_class['#funcs']['#attributes']
current_access = Access.PUBLIC
current_type = None
is_param = False
param_count = 0
var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT)
temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)


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
  global current_class, current_function, current_access, var_avail, temp_avail
  current_class = classes['#global']
  current_function = current_class['#funcs']['#attributes']
  current_access = Access.PUBLIC
  var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT)
  temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)


def seen_func(func_name):
  global func_size, current_class, current_function, var_avail, temp_avail
  func_size = 0
  if func_name in current_class['#funcs']:
    return f"Redeclared function {func_name}"
  else:
    current_class['#funcs'][func_name] = new_func_dict(func_name, current_type)
    current_function = current_class['#funcs'][func_name]
  var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT)
  temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)


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
  global param_count
  if var_name in current_function['#vars']:
    return f"Redeclared variable: {var_name}"
  else:
    address = var_avail.next(current_type)
    if not address:
      return 'Too many variables.'
    adjust = 0
    if current_function['#name'] == '#attributes':
      adjust = ATTRIBUTES_ADJUSTMENT
      if current_class['#name'] == '#global':
        adjust = GLOBAL_ADJUSTMENT

    current_function['#vars'][var_name] = (
        new_var_dict(current_type, address-adjust, current_access))

    if is_param:
      current_function['#param_count'] += 1
      current_function['#vars'][var_name]['#assigned'] = True
    else:
      current_function['#var_count'] += 1


def switch_param(reading_params):
  global is_param
  is_param = reading_params


def set_access():
  global current_function
  current_function['#access'] = current_access


# Intermediate code generation.

operators = []
types = []
operands = []
quadruples = [[Operations.GOTO.value, None, None, None]]
visual_quadruples = [[Operations.GOTO.name, None, None, None]]
jumps = []
pending_returns = []
q_count = 1
const_avail = Available(CONSTANT_LOWER_LIMIT, CONSTANT_UPPER_LIMIT,
                        avail_types)
constant_addresses = {}
calling_class = current_class
expecting_init = False
calling_parent = False
class_call_stack = []
func_call_stack = []
params_stack = []


def address_or_else(operand, is_visual=False):
  if operand is not None:
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


def find_and_populate(operand, prefix, access, check_assigned_var=False,
                      mark_assigned=False, check_init_called=False):
  global expecting_init
  raw_operand = operand.get_raw()
  var = prefix.get(raw_operand, None)
  if not var:
    return False
  if check_init_called:
    if not var['#assigned']:
      expecting_init = True
      var['#assigned'] = True
  if check_assigned_var:
    if mark_assigned:
      var['#assigned'] = True
    elif not var['#assigned']:
      operand.set_error(f'Variable {raw_operand} used before assignment.')
      return True
  if var['#access'] not in access:
    operand.set_error(f'Variable {raw_operand} cannot be accessed.')
    return True
  else:
    operand.set_type(var['#type'])
    operand.set_address(var['#address'])
    return True


def populate_instance_call(operand, check_init_called=True):
  # Search for var in the attributes of the class and its parents.
  curr_class = calling_class['#name']
  while curr_class:
    class_attributes = classes[curr_class]['#funcs']['#attributes']['#vars']
    if find_and_populate(operand, class_attributes, [Access.PUBLIC], False,
                         False, check_init_called):
      return
    curr_class = classes[curr_class]['#parent']

  if not operand.get_error():
    operand.set_error(f'{operand.get_raw()} not in scope.')


def populate_instance_func_call(func_data, is_init=False):
  global expecting_init
  func_name = func_data.func_name

  if is_init:
    expecting_init = False
  curr_class = calling_class['#name']
  while curr_class:
    if func_name in classes[curr_class]['#funcs']:
      if classes[curr_class]['#funcs'][func_name]['#access'] != Access.PUBLIC:
        func_data.error = f"Cannot access {func_name}."
        return
      func_data.func_type = classes[curr_class]['#funcs'][func_name]['#type']
      func_data.class_name = curr_class
      return
    curr_class = classes[curr_class]['#parent']

  if not func_data.error:
    func_data.error = f'{func_name} not defined in scope.'


def populate_local_var(operand, mark_assigned=False, is_instance=False):
  # Search for var in function's local vars.
  check_assigned_var = not is_instance
  function_vars = current_function['#vars']
  if find_and_populate(operand, function_vars,
                       [Access.PUBLIC, Access.PROTECTED, Access.PRIVATE],
                       check_assigned_var, mark_assigned, is_instance):
    return
  # Search for var in the attributes from the class.
  class_attributes = current_class['#funcs']['#attributes']['#vars']
  if find_and_populate(operand, class_attributes,
                       [Access.PUBLIC, Access.PROTECTED, Access.PRIVATE],
                       check_assigned_var, mark_assigned, is_instance):
    return
  # Search for var in the attributes of inherited classes.
  curr_class = current_class['#parent']
  while curr_class:
    class_attributes = classes[curr_class]['#funcs']['#attributes']['#vars']
    if find_and_populate(operand, class_attributes,
                         [Access.PUBLIC, Access.PROTECTED],
                         check_assigned_var, mark_assigned, is_instance):
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


def find_and_build_operand(raw_operand, mark_assigned=False):
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
      address = get_or_create_cte_address(raw_operand[1:-1], Types.CHAR)
      if not address:
        operand.set_error('Too many char constants.')
      operand.set_type(Types.CHAR)
      operand.set_address(address)
      operand.set_raw(raw_operand[1:-1])
    else:
      populate_local_var(operand, mark_assigned)
  return operand


def register_operand(raw_operand, mark_assigned=False):
  global operands, types
  operand = find_and_build_operand(raw_operand, mark_assigned)
  if operand.get_error():
    return operand.get_error()
  operands.append(operand)
  types.append(operand.get_type())


def register_operator(operator):
  global operators
  operators.append(operator)


def build_temp_operand(op_type, assignable=False):
  global current_function
  operand = Operand()
  address = temp_avail.next(op_type)
  if not address:
    operand.set_error('Too many variables.')
  current_function['#vars'][address] = new_var_dict(
      op_type, address, assigned=True)
  current_function['#var_count'] += 1
  operand.set_address(address)
  operand.set_type(op_type)
  operand.set_raw(operand.get_address())
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


def do_assign():
  global operators, operands, types
  left_operand = operands.pop()
  left_type = types.pop()
  assigning_operand = operands.pop()
  assigning_type = types.pop()
  if not semantic_cube[assigning_type][left_type][Operations.EQUAL]:
    if left_type == Types.VOID:
      return f'Expression returns no value.'
    return (f'Type mismatch: expression cannot be assigned')
  generate_quadruple(Operations.EQUAL, left_operand, None, assigning_operand)
  operands.append(assigning_operand)
  types.append(assigning_type)


def do_write(s=None):
  global operands, types
  if s:
    operand = Operand(s[1:-1])
    operand.set_type(Types.CTE_STRING)
    operand.set_address(s[1:-1])
  else:
    operand = operands.pop()
    op_type = types.pop()
    if op_type not in var_types:
      return f'Expression returns no value.'
  generate_quadruple(Operations.WRITE, None, None, operand)


def do_read():
  global operands, types
  operand = Operand('read')
  operand.set_address('read')
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
  quadruples[end][3] = q_count+1
  ret = jumps.pop()
  generate_quadruple(Operations.GOTO, None, None, ret)


def register_function_beginning():
  current_function['#start'] = q_count


def set_current_type_void():
  global current_type
  current_type = Types.VOID


def register_main_beginning():
  quadruples[0][3] = q_count
  visual_quadruples[0][3] = q_count


def register_func_end(is_main=False):
  global pending_returns
  if current_function['#type'] != Types.VOID and len(pending_returns) == 0:
    return f"No return statement on non-void function {current_function['#name']}"
  while len(pending_returns):
    quadruples[pending_returns.pop()][3] = q_count
  if is_main:
    generate_quadruple(Operations.END, None, None, None)
  else:
    generate_quadruple(Operations.ENDPROC, None, None, None)


def register_return():
  global operands, types, pending_returns
  function_type = current_function['#type']
  if function_type == Types.VOID:
    return 'Void function cannot return a value'
  return_val = operands.pop()
  return_type = types.pop()
  if not semantic_cube[function_type][return_type][Operations.EQUAL]:
    return f'Cannot return type {return_type} as {function_type}'
  pending_returns.append(q_count)
  generate_quadruple(Operations.RETURN, return_val, None, None)


def switch_instance(instance_name, is_first=False):
  global calling_class

  if is_first:
    class_call_stack.append([])

  instance = Operand(instance_name)
  if len(class_call_stack[-1]) == 0:
    populate_local_var(instance, is_instance=True)
  else:
    calling_class = classes[class_call_stack[-1][-1].get_type()]
    populate_instance_call(instance)

  if instance.get_error():
    return instance.get_error()

  class_call_stack[-1].append(instance)


def seen_instance_attribute(attribute_name):
  global calling_class
  attribute = Operand(attribute_name)
  calling_class = classes[class_call_stack[-1][-1].get_type()]
  populate_instance_call(attribute)

  if attribute.get_error():
    return attribute.get_error()

  for instance in class_call_stack[-1]:
    generate_quadruple(Operations.ENTER_INSTANCE, instance,
                       None, instance.get_type())

  generate_quadruple(Operations.RETURN, attribute, None, q_count+1)

  while len(class_call_stack[-1]) > 0:
    generate_quadruple(Operations.EXIT_INSTANCE, None, None, None)
    class_call_stack[-1].pop()

  if attribute.get_type() in var_types:
    temp = build_temp_operand(attribute.get_type())
    generate_quadruple(Operations.GET_RETURN, temp, None, None)
    operands.append(temp)
    types.append(temp.get_type())
  else:
    return f'Invalid return type on expression.'


def seen_instance_func(func_name, is_init=False):
  global calling_class
  func_data = FuncData(func_name)
  calling_class = classes[class_call_stack[-1][-1].get_type()]
  populate_instance_func_call(func_data, is_init=is_init)

  if func_data.error:
    return func_data.error

  func_call_stack.append(func_data)


def call_parent(parent):
  global calling_class, calling_parent
  if not current_class['#parent']:
    return (f"{current_class['#name']} has no parent class but tries "
            + f'to extend {parent} in constructor')
  elif parent != current_class['#parent']:
    return f"{parent} is not {current_class['#name']}'s parent"
  calling_parent = True
  calling_class = classes[parent]

  class_op = Operand(classes[parent]['#name'])
  class_op.set_type(classes[parent]['#name'])
  class_call_stack.append([class_op])

  classes[classes[parent]['#name']]['#funcs']['init']

  func_data = FuncData('init')
  func_data.func_type = Types.VOID
  func_data.class_name = classes[parent]['#name']

  func_call_stack.append(func_data)


def populate_local_func_call(func_data):
  func_name = func_data.func_name
  if func_name in calling_class['#funcs']:
    if calling_class['#funcs'][func_name]['#access'] != Access.PUBLIC:
      func_data.error = f'{func_name} not in scope.'
  func_data.func_type = calling_class['#funcs'][func_name]['#type']


def seen_local_func(func_name):
  global calling_class

  func_data = FuncData(func_name)
  calling_class = current_class
  populate_local_func_call(func_data)
  func_data.class_name = current_class['#name']

  if func_data.error:
    return func_data.error

  class_op = Operand(current_class['#name'])
  class_op.set_type(current_class['#name'])
  class_call_stack.append([class_op])

  func_call_stack.append(func_data)


def start_passing_params():
  operators.append(Operations.FAKE_BOTTOM)
  params_stack.append([])


def register_param():
  params_stack[-1].append(operands.pop())


def done_passing_params(is_local=False):
  if not is_local:
    for instance in class_call_stack[-1]:
      generate_quadruple(Operations.ENTER_INSTANCE, instance,
                        None, instance.get_type())
  generate_quadruple(Operations.ERA, func_call_stack[-1].class_name,
                     func_call_stack[-1].func_name, None)

  func = classes[func_call_stack[-1].class_name]['#funcs'][func_call_stack[-1].func_name]

  expecting_params = func['#param_count']
  assigning_params = list(func['#vars'].values())
  if len(params_stack[-1]) != expecting_params:
    return (f"{func['#name']} expects {expecting_params}, but "
            + f'{len(params_stack[-1])} were given')
  count = 0
  for sending_param in params_stack[-1]:
    if not semantic_cube[assigning_params[count]['#type']][sending_param.get_type()][Operations.EQUAL]:
      return (f'Incompatible param {count+1} on call to ' +
          f"{func['#name']}")
    generate_quadruple(Operations.PARAM, sending_param, None, count)
    count += 1
  params_stack.pop()

  generate_quadruple(Operations.GOSUB, func_call_stack[-1].class_name,
                     func_call_stack[-1].func_name, None)

  if not is_local:
    while len(class_call_stack[-1]) > 0:
      generate_quadruple(Operations.EXIT_INSTANCE, None, None, None)
      class_call_stack[-1].pop()
  class_call_stack.pop()


  if func_call_stack[-1].func_type in var_types:
    temp = build_temp_operand(func_call_stack[-1].func_type)
    generate_quadruple(Operations.GET_RETURN, temp, None, None)
    operands.append(temp)
    types.append(temp.get_type())
  else:
    operands.append(Types.VOID)
    types.append(Types.VOID)
  func_call_stack.pop()

  operators.pop()


def generate_output():
  global classes

  data_segment = {}
  for v in classes['#global']['#funcs']['#attributes']['#vars'].values():
    if type(v['#type']) == str:
      var_type = v['#type']
    else:
      var_type = v['#type'].value
    data_segment[v['#address']] = var_type

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
