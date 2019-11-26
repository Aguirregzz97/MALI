# Semantic checks and quadruple generation for MALI language.

from implementation.utils.semantic_and_quadruples_utils import *  # pylint: disable=unused-wildcard-import
from implementation.utils.generic_utils import *
from implementation.utils.constants import *
import re
import copy


# Semantic table filling.

classes = {'#global': new_class_dict(name='#global', parent=None)}
'''Symbol table.'''

current_class = classes['#global']
'''Keeps track of the class that is being parsed.'''

current_function = current_class['#funcs']['#attributes']
'''Keeps track of the function that is being parsed.'''

current_access = Access.PUBLIC
'''Keeps track of the current access type.'''

current_type = None
'''Keeps track of the currect data type.'''

is_param = False
'''Set to True when reading params declaration. Used  to increase the count
   of parameters of a function in the symbol table.'''

var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT)
'''Provides methods to get the next available address for a variable of a given
   data type. Resetted for every new function.'''

temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)
'''Provides methods to get the next available address for a temporary of a given
   data type. Resetted for every new function.'''

last_declared_var = None
'''Keeps track of the last variable that was declared. Used for defining
   dimensions.'''

r = None
'''Keeps track of the r-value when calculating the total space occupied by a
   dimensionated variable. Resseted for every new dimensionated variable.'''


def seen_class(class_name: str):
  '''Registers a new class.

  Returns error if the class name was already used.
  '''
  if class_name in classes:
    return f"Repeated class name: {class_name}"
  else:
    global current_class, current_function
    classes[class_name] = new_class_dict(class_name)
    current_class = classes[class_name]
    current_function = current_class['#funcs']['#attributes']


def class_parent(class_parent: str):
  '''Registers the parent that the current class inherits from.

  Returns error if parent does not exist.
  '''
  if class_parent not in classes:
    return f"Undeclared class parent: {class_parent}"

  current_class['#parent'] = class_parent

  current_class['#funcs']['#attributes']['#vars'] = copy.deepcopy(
      classes[class_parent]['#funcs']['#attributes']['#vars'])

  for var in current_class['#funcs']['#attributes']['#vars'].values():
    var_avail.next(var['#type'])
    var['#inherited'] = True


def finish_class():
  '''Prepares variables for the next class to be parsed.'''
  global current_class, current_function, current_access, var_avail, temp_avail

  current_class = classes['#global']
  current_function = current_class['#funcs']['#attributes']
  current_access = Access.PUBLIC
  var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT)
  temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)


def seen_func(func_name: str):
  '''Registers a new function.

  Returns error if the function name was already used within the class.
  '''
  global func_size, current_class, current_function, var_avail, temp_avail
  func_size = 0
  if func_name in current_class['#funcs']:
    return f"Redeclared function \'{func_name}\'"
  else:
    current_class['#funcs'][func_name] = new_func_dict(func_name, current_type)
    current_function = current_class['#funcs'][func_name]
  var_avail = Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT)
  temp_avail = Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT)


def seen_access(new_access: Access):
  '''Registers the read access type.'''
  global current_access
  current_access = new_access


def seen_type(new_type: Types):
  '''Registers the read data type.

  Returns error if data type does not exist (Ex.: Creating an instance of a
  non-existent class).
  '''
  global current_type
  if new_type not in func_types and (
          new_type not in classes):
    return f"\'{new_type}\' is not a class nor data type"
  current_type = new_type


def var_name(var_name: str, assigned=False):
  '''Registers the read variable.

  Returns error if variable is redeclared.
  Returns error if function runs out of variable addresses.
  '''
  global last_declared_var
  adjust = 0
  if (var_name in current_function['#vars'] and
          not current_function['#vars'][var_name]['#inherited']):
    return f"Redeclared variable: {var_name}"
  if (var_name in current_function['#vars'] and
      current_function['#vars'][var_name]['#inherited'] and
          current_function['#vars'][var_name]['#access'] != Access.PRIVATE):
    address = current_function['#vars'][var_name]['#address']
  else:
    address = var_avail.next(current_type)
    if not address:
      return 'Too many variables.'
    if current_function['#name'] == '#attributes':
      adjust = ATTRIBUTES_ADJUSTMENT
      assigned = True
      if current_class['#name'] == '#global':
        adjust = GLOBAL_ADJUSTMENT
        assigned = True

  if is_param:
    current_function['#param_count'] += 1
    assigned = True

  current_function['#vars'][var_name] = (
      new_var_dict(current_type, address-adjust, current_access,
                   assigned=assigned))

  last_declared_var = var_name


def switch_param(reading_params: bool):
  '''Switches is_param flag.'''
  global is_param
  is_param = reading_params


def set_access():
  '''Sets current function with the current access.'''
  global current_function
  current_function['#access'] = current_access


# Intermediate code generation.

quadruples = [[Operations.GOTO.value, None, None, None]]
'''Saves generated quadruples.'''

q_count = 1
'''Counter that keeps track of the position of the next quadruple to be
   generated.'''

# TODO: remove.
visual_quadruples = [[Operations.GOTO.name, None, None, None]]
'''Saves a visual representation of the generated quadruples, used for
   debugging.'''

const_avail = Available(CONSTANT_LOWER_LIMIT, CONSTANT_UPPER_LIMIT)
'''Provides methods to get the next available address for a const of a given
   data type.'''

constants_with_addresses = {
    Types.INT: {},
    Types.FLOAT: {},
    Types.CHAR: {},
    Types.BOOL: {},
}
'''Generated constants annotated with their address.'''

operator_stack = []
'''Operator stack used for expression parsing.'''

# TODO: remove types stack, since operand_stack receives Operand class
# instances, which track data type.
type_stack = []
'''Types stack used for expression parsing.'''

operand_stack = []
'''Operand stack used for expression parsing.'''

jump_stack = []
'''Jump stack used for parsing control structures.'''

pending_returns = []
'''List that keeps track of generated return quadruples. These quadruples
   will be updated with the position of the function end quadruple (ENDPROC),
   so the vm knows where to jump after a return.'''

owner_class = current_class
'''Keeps track of the class that owns the method that is being called.'''

expecting_init = False
'''Set to True when a called instance has not been initialized. Used to ensure
   that init is called after seing the instance.'''

# TODO: add link to documentation: function/method call parsing.

class_call_stack = []
'''Class call stack used to parse function and method calls.'''

proc_call_stack = []
'''Function call stack used to parse function and method calls.'''

param_stack = []
'''Params stack used to parse function and method calls.'''

pila_dimensionada = []
'''Dimensions stack used to parse dimensionated variable accesses.'''


def address_or_else(operand: Operand, is_visual=False):
  '''Used by generate_quadruple() to generate visual quadruples.

  Returns operand address if is_visual is set to False.
  Returns operand raw value if is_visual is set to True.
  '''
  if operand is not None:
    if isinstance(operand, Operand):
      if is_visual:
        return operand.get_raw()
      else:
        return operand.get_address()
    else:
      return operand
  return None


def generate_quadruple(a: Operations, b: Operand, c: Operand, d: Operand):
  '''Generates quadruple and appends to quadruples list.

  Also generates visual quadruple and appens to visual_quadruples list.
  '''
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


def find_and_populate(operand: Operand, prefix: dict, access: [Access],
                      check_assigned_var=False, mark_assigned=False,
                      check_init_called=False):
  '''Searches for a variable/attribute.

  Generic function called by other searching functions.

  Searches for a variable/attribute starting from a given place (param prefix)
  in the symbol table and validates that its access matches the provided
  accesses (param access).

  Populates the operand (param operand) with its address and type.

  if check_assigned_var is set to True, and the variable/attribute has not been
  assigned yet, populates the operand's error attribute.

  if mark_assigned is set to True, sets the variable/attribute to assigned.

  if check_init_called is set to True, sets the instance to initialized.

  Returns True if variable/attribute was found.
  Returns False if variable/attribute was not found.
  '''
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
      operand.set_error(f'Variable \'{raw_operand}\' used before assignment.')
      return True
  if var['#access'] not in access:
    operand.set_error(f'Variable \'{raw_operand}\' cannot be accessed.')
    return True
  elif var['#inherited'] and var['#access'] == Access.PRIVATE:
    return False
  else:
    operand.set_type(var['#type'])
    operand.set_address(var['#address'])
    return True


def populate_instance_attribute_call(operand: Operand, check_init_called=True):
  '''Search for attribute in owner_class and its parents.

  Used to search for attributes within instances.

  Populate param operand with type and address.

  Returns error if function is not found / out of scope.
  Returns error if operand has error.
  '''
  class_attributes = (classes[owner_class['#name']]
                             ['#funcs']['#attributes']['#vars'])
  if find_and_populate(operand, class_attributes, [Access.PUBLIC], False,
                       False, check_init_called):
    return

  if not operand.get_error():
    operand.set_error(f'\'{operand.get_raw()}\' not in scope.')


def populate_instance_func_call(func_data: FuncData, is_init=False):
  '''Search for a function in owner_class and its parents.

  Populate param func_data with its type and defining class.

  Returns error if function is not found / out of scope.
  Returns error if operand has error.
  '''
  global expecting_init
  func_name = func_data.func_name

  if is_init:
    expecting_init = False
  curr_class = owner_class['#name']
  while curr_class:
    if (func_name in classes[curr_class]['#funcs'] and
            classes[curr_class]['#funcs'][func_name]['#access'] == Access.PUBLIC):
      func_data.func_type = classes[curr_class]['#funcs'][func_name]['#type']
      func_data.class_name = curr_class
      return
    curr_class = classes[curr_class]['#parent']

  if not func_data.error:
    func_data.error = f'\'{func_name}\' not defined in scope.'


def populate_local_var(operand: Operand, mark_assigned=False,
                       is_instance=False):
  '''Search for var/attribute in function local vars, function's class, and
     parents

  Populate operand with address and type.

  Returns error if not found.
  Returns error if operand has error.
  '''
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

  # Search for var in the global vars from the class.
  global_vars = classes['#global']['#funcs']['#attributes']['#vars']
  if find_and_populate(operand, global_vars,
                       [Access.PUBLIC, Access.PROTECTED, Access.PRIVATE],
                       check_assigned_var, mark_assigned, is_instance):
    return

  if not operand.get_error():
    operand.set_error(f'Variable \'{operand.get_raw()}\' not in scope.')


def populate_local_func_call(func_data: FuncData):
  '''Finds func in class and parents, and popualtes FuncData.'''
  func_name = func_data.func_name
  if func_name in owner_class['#funcs']:
    func_data.func_type = owner_class['#funcs'][func_name]['#type']
    func_data.class_name = owner_class['#name']
    return

  curr_class = owner_class['#parent']
  while curr_class:
    if (func_name in classes[curr_class]['#funcs'] and
            classes[curr_class]['#funcs'][func_name]['#access'] != Access.PRIVATE):
      func_data.func_type = classes[curr_class]['#funcs'][func_name]['#type']
      func_data.class_name = curr_class
      return
    curr_class = classes[curr_class]['#parent']

  if func_name in classes['#global']['#funcs']:
    func_data.func_type = classes['#global']['#funcs'][func_name]['#type']
    func_data.class_name = '#global'
    return

  func_data.error = f'\'{func_name}\' not in scope.'


def get_or_create_cte_address(value, val_type):
  '''Returns address for a constant value.

  Creates and returns address for constant, or returns address if it was
  already created.

  Returns error if there are no more addresses available.
  '''
  global constants_with_addresses
  if value in constants_with_addresses[val_type]:
    return constants_with_addresses[val_type][value]
  else:
    address = const_avail.next(val_type)
    if not address:
      return f'Too many \'{val_type}\' constants'
    constants_with_addresses[val_type][value] = address
    return address


def find_and_build_operand(raw_operand, mark_assigned=False):
  '''Build Operand class from raw value operand.

  Build operand from raw_operand, where raw_operand can be a constant value,
  or a var/attribute. If it is a var/attribute, search for it starting from
  the current class.

  Sets operand to error if it runs out of addresses for a data type.
  Sets operand to error if var/attribute was not found.
  '''
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
    if re.match(r'\'(.|\\.)\'', raw_operand):
      if re.match(r'\'\\.\'', raw_operand):
        char_raw_operand = ord(raw_operand[1:-1].encode('utf-8')
                                                .decode('unicode_escape'))
      else:
        char_raw_operand = ord(raw_operand[1:-1])
      address = get_or_create_cte_address(char_raw_operand, Types.CHAR)
      if not address:
        operand.set_error('Too many char constants.')
      operand.set_type(Types.CHAR)
      operand.set_address(address)
      operand.set_raw(char_raw_operand)
    else:
      populate_local_var(operand, mark_assigned)
  return operand


def register_operand(raw_operand, mark_assigned=False):
  '''Build an Operand object from a raw_operand and append it to operand stack.

  Build an Operand from a raw_operand, which can be a constant value or a
  variable/attribute, and append the resulting operand to the operand stack
  and its type to the type stack.

  Return error if Operand was populated with error.
  '''
  global operand_stack, type_stack
  operand = find_and_build_operand(raw_operand, mark_assigned)
  if operand.get_error():
    return operand.get_error()
  operand_stack.append(operand)
  type_stack.append(operand.get_type())


def register_operator(operator: str):
  '''Append the received operator to the operator stack.'''
  global operator_stack
  operator_stack.append(operator)


def build_temp_operand(op_type: Types, assignable=False):
  '''Build a temp variable of a given type in the current function.

  Returns error if it runs out of addresses.
  '''
  global current_function
  operand = Operand()
  address = temp_avail.next(op_type)
  if not address:
    operand.set_error('Too many variables.')
  current_function['#vars'][address] = new_var_dict(
      op_type, address, assigned=True)
  operand.set_address(address)
  operand.set_type(op_type)
  operand.set_raw(operand.get_address())
  return operand


def solve_operation_or_continue(ops: [Operations]):
  '''Generates quadruple for next operation if it exists in ops.

  Solves the next operation (from the operation stack) if it is included in ops.

  Returns error if operation cannot be performed on the given operands.
  Returns error if trying to perform an operation on a call to a void function.
  '''
  global operator_stack, operand_stack, type_stack
  operator = top(operator_stack)
  if operator in ops:
    right_operand = operand_stack.pop()
    right_type = type_stack.pop()
    left_operand = operand_stack.pop()
    left_type = type_stack.pop()
    operator = operator_stack.pop()
    result_type = semantic_cube[left_type][right_type][operator]
    if not result_type:
      if left_type == Types.VOID or right_type == Types.VOID:
        return f'Expression returns no value.'
      return f'Type mismatch: Invalid operation \'{operator}\' on given operand'
    temp = build_temp_operand(result_type)
    if temp.get_error():
      return temp.get_error()
    generate_quadruple(operator, left_operand, right_operand, temp)
    operand_stack.append(temp)
    type_stack.append(result_type)


def solve_if_unary_operation():
  operator = top(operator_stack)
  if (operator in
          (Operations.PLUS_UNARY, Operations.MINUS_UNARY, Operations.NOT)):
    operand = operand_stack.pop()
    op_type = type_stack.pop()
    result_type = semantic_cube[op_type][operator]
    operator = operator_stack.pop()
    if not result_type:
      if op_type == Types.VOID:
        return f'Expression returns no value.'
      return f'Type mismatch: Invalid operation \'{operator.name}\' on given operand'
    temp = build_temp_operand(result_type)
    if temp.get_error():
      return temp.get_error()
    generate_quadruple(operator, operand, None, temp)
    operand_stack.append(temp)
    type_stack.append(result_type)


def pop_fake_bottom():
  '''Pops fake bottom from the operator stack.'''
  global operator_stack
  operator_stack.pop()


def do_assign():
  '''Generates quadruple for the assignment operation.

  Returns error if expression cannot be assigned to variable.
  Returns error if trying to assign a call to a void function.
  '''
  global operator_stack, operand_stack, type_stack
  left_operand = operand_stack.pop()
  left_type = type_stack.pop()
  assigning_operand = operand_stack.pop()
  assigning_type = type_stack.pop()
  if not semantic_cube[assigning_type][left_type][Operations.EQUAL]:
    if left_type == Types.VOID:
      return f'Expression returns no value.'
    return f'Type mismatch: expression cannot be assigned'
  generate_quadruple(Operations.EQUAL, left_operand, None, assigning_operand)
  operand_stack.append(assigning_operand)
  type_stack.append(assigning_type)


def do_write(s=None):
  '''Generate quadruple for the write operation.

  Can write either the result of an expression or a given string.

  Returns error if trying to print a call to a void function.
  '''
  global operand_stack, type_stack
  if s:
    operand = Operand(s[1:-1])
    operand.set_type(Types.CTE_STRING)
    operand.set_address(s[1:-1])
  else:
    operand = operand_stack.pop()
    op_type = type_stack.pop()
    if op_type not in var_types:
      return f'Expression returns no value.'
  generate_quadruple(Operations.WRITE, None, None, operand)


def do_read():
  '''Append the read opperand to the operand stack.

  This operand will trigger the virtual machine to read from terminal.
  '''
  global operand_stack, type_stack
  operand = Operand('#read')
  operand.set_address('#read')
  operand.set_type(Types.READ)
  operand_stack.append(operand)
  type_stack.append(Types.READ)


def register_condition():
  '''Generates de quadruple for when a condition is seen.

  Returns error if the operand is not boolean.
  '''
  global operand_stack, type_stack
  exp_type = type_stack.pop()
  if exp_type not in var_types:
    return 'Evaluated expression is not boolean'
  result = operand_stack.pop()
  generate_quadruple(Operations.GOTOF, result, None, None)
  jump_stack.append(q_count-1)


def register_else():
  '''Generates goto quadruple for else block in an if.

  Generates goto quadruple after instructions of the true block of the if, and
  appends it to the jump stack, to add the position when it is known.
  Pops from the jump stack the goto-false quadruple from the if begining, and
  sets the position.
  '''
  generate_quadruple(Operations.GOTO, None, None, None)
  false = jump_stack.pop()
  jump_stack.append(q_count-1)
  quadruples[false][3] = q_count


def register_end_if():
  '''Add position to the goto quadruple of the true block of the if.'''
  end = jump_stack.pop()
  quadruples[end][3] = q_count


def register_while():
  '''Append while start to the jump stack.'''
  jump_stack.append(q_count)


def register_end_while():
  '''Generate goto quadruple to return to while condition'''
  end = jump_stack.pop()
  quadruples[end][3] = q_count+1
  ret = jump_stack.pop()
  generate_quadruple(Operations.GOTO, None, None, ret)


def register_function_beginning():
  '''Register quadruple where the function starts.

  This will be used by the vm to know where to go when getting the gosub
  operation.
  '''
  current_function['#start'] = q_count


def set_current_type_void():
  '''Sets current type to void.

  Used when parsing the main function and constructors.
  '''
  global current_type
  current_type = Types.VOID


def register_main_beginning():
  '''Sets the position where the main function starts on the initial
     quadruple.'''
  quadruples[0][3] = q_count
  visual_quadruples[0][3] = q_count


def register_func_end(is_main=False):
  '''Actions for when the function is finished.

  Generate endproc quadruple (or end quadruple if finished main).

  Returns error if non-void function has no returns.
  '''
  global pending_returns
  if current_function['#type'] != Types.VOID and len(pending_returns) == 0:
    return ('No return statement on non-void function' +
            f"\'{current_function['#name']}\'")
  while len(pending_returns):
    quadruples[pending_returns.pop()][3] = q_count
  if is_main:
    generate_quadruple(Operations.END, None, None, None)
  else:
    generate_quadruple(Operations.ENDPROC, None, None, None)

  # Delete the function's variables (but not the parameters).
  count = 0
  for var in current_function['#vars']:
    if count > current_function['#param_count']:
      del var
    count += 1


def register_return():
  '''Generate return quadruple.

  Add generated return to pending_return list, so the position of the endproc
  quadruple is added when known.

  Returns error if called by void function.
  Returns error if returning value type cannot be assigned to function's return
  type.
  '''
  global operand_stack, type_stack, pending_returns
  function_type = current_function['#type']
  if function_type == Types.VOID:
    return 'Void function cannot return a value'
  return_val = operand_stack.pop()
  return_type = type_stack.pop()
  if not semantic_cube[function_type][return_type][Operations.EQUAL]:
    return f'Cannot return type \'{return_type}\' as \'{function_type}\''
  pending_returns.append(q_count)
  generate_quadruple(Operations.RETURN, return_val, None, None)


def switch_instance(instance_name: str, is_first=False):
  '''Register instance switch.

  Populate an operand for the instance.
  If this is the first instance call in a row: append a list to
  class_call_stack.
  Save the operand to the top list of class_call_stack.

  Returns error if operand has error.
  '''
  global owner_class

  if expecting_init:
    return 'Calling class member before calling init.'

  if is_first:
    class_call_stack.append([])

  instance = Operand(instance_name)
  if len(class_call_stack[-1]) == 0:
    populate_local_var(instance, is_instance=True)
  else:
    owner_class = classes[class_call_stack[-1][-1].get_type()]
    populate_instance_attribute_call(instance)

  if instance.get_error():
    return instance.get_error()

  class_call_stack[-1].append(instance)


def seen_instance_attribute(attribute_name):
  '''Actions on call to instance attribute.

  Populates operand from attribute.
  Generates enter instance quadruples for every instance in the top list of
  class_call_stack.
  Generates return for the called attribute.
  Generates enter instance quadruples for every instance in the top list of
  class_call_stack.
  Generates get_return quadruple to get the result of the called attribute.

  Returns error if operand has error.
  '''
  global owner_class

  if expecting_init:
    return 'Calling class member before calling init.'

  attribute = Operand(attribute_name)
  owner_class = classes[class_call_stack[-1][-1].get_type()]
  populate_instance_attribute_call(attribute)

  if attribute.get_error():
    return attribute.get_error()

  for instance in class_call_stack[-1]:
    generate_quadruple(Operations.ENTER_INSTANCE, instance,
                       None, instance.get_type())

  generate_quadruple(Operations.RETURN, attribute, None, q_count+1)

  while len(class_call_stack[-1]) > 0:
    generate_quadruple(Operations.EXIT_INSTANCE, None, None, None)
    class_call_stack[-1].pop()
  class_call_stack.pop()

  if attribute.get_type() in var_types:
    temp = build_temp_operand(attribute.get_type())
    generate_quadruple(Operations.GET_RETURN, temp, None, None)
    operand_stack.append(temp)
    type_stack.append(temp.get_type())
  else:
    return f'Invalid return type on expression.'


def seen_assigning_instance_attribute(attribute_name: str):
  '''Register attribute that will be assigned ones the expression is parsed.

  Returns error if attribute is not found or is not accessible.
  '''
  global owner_class

  attribute = Operand(attribute_name)
  owner_class = classes[class_call_stack[-1][-1].get_type()]
  populate_instance_attribute_call(attribute)

  if attribute.get_error():
    return attribute.get_error()

  proc_call_stack.append(attribute)


def assign_instance_attribute():
  '''Perform assignement on instance attribute.

  Returns error if types cannot be assigned.
  '''
  for instance in class_call_stack[-1]:
    generate_quadruple(Operations.ENTER_INSTANCE, instance,
                       None, instance.get_type())

  attribute = proc_call_stack.pop()
  assigning = operand_stack.pop()

  if not (semantic_cube[attribute.get_type()][assigning.get_type()]
                       [Operations.EQUAL]):
    print(assigning.get_type(), attribute.get_type())
    return 'Incompatible types on assignment.'

  generate_quadruple(Operations.SET_FOREIGN, None, None, None)
  generate_quadruple(Operations.PARAM, assigning, None, attribute)
  generate_quadruple(Operations.UNSET_FOREIGN, None, None, None)

  while len(class_call_stack[-1]) > 0:
    generate_quadruple(Operations.EXIT_INSTANCE, None, None, None)
    class_call_stack[-1].pop()
  class_call_stack.pop()


def seen_instance_func(func_name: str, is_init=False):
  '''Register call to a function from an instance.

  Populate FuncData from func name.
  Append func to proc_call_stack.

  Return error if FuncData has error.
  '''
  global owner_class
  func_data = FuncData(func_name)
  owner_class = classes[class_call_stack[-1][-1].get_type()]
  populate_instance_func_call(func_data, is_init=is_init)

  if func_data.error:
    return func_data.error

  proc_call_stack.append(func_data)


def call_parent(parent_name: str):
  '''Prepare the call to an inherited parent method.

  Populate operand with parent name and append to class_call_stack.
  Populate FuncData with parent's init and append to proc_call_stack.

  Return error if class had no defined parent.
  Return error if operan has error.
  '''
  global owner_class
  if not current_class['#parent']:
    return (f"\'{current_class['#name']}\' has no parent class but tries "
            + f'to extend \'{parent_name}\' in constructor')
  elif parent_name != current_class['#parent']:
    return f"\'{parent_name}\' is not \'{current_class['#name']}'s\' parent"
  owner_class = classes[parent_name]

  class_op = Operand(classes[parent_name]['#name'])
  class_op.set_type(classes[parent_name]['#name'])
  class_call_stack.append([class_op])

  classes[classes[parent_name]['#name']]['#funcs']['init']

  func_data = FuncData('init')
  func_data.func_type = Types.VOID
  func_data.class_name = classes[parent_name]['#name']

  proc_call_stack.append(func_data)


def seen_local_func(func_name: str):
  '''Actions on call to local function.

  Append operand with current class to class_call_stack.
  Append FuncData to proc_call_stack.

  Return error if FuncData has error.
  '''
  global owner_class

  func_data = FuncData(func_name)
  owner_class = current_class
  populate_local_func_call(func_data)

  if func_data.error:
    return func_data.error

  class_op = Operand(current_class['#name'])
  class_op.set_type(current_class['#name'])
  class_call_stack.append([])

  proc_call_stack.append(func_data)


def start_passing_params():
  '''Prepares to receive params by appending empty list to param_stack.'''
  operator_stack.append(Operations.FAKE_BOTTOM)
  param_stack.append([])


def register_param():
  '''Appends evaluated expression to top list in param_stack'''
  param = operand_stack.pop()
  if param == Types.VOID:
    return 'Expression returns no value.'
  param_stack[-1].append(param)


def done_passing_params(is_local=False):
  '''Generates quadruple for calling function.

  If not local, generate quadruple enter instance for every instance in top list
  of class_call_stack.
  Pass every param on top list of param_stack.
  Generate gosub quadruple.
  If not local, generate quadruple exit instance for every instance in top list
  of class_call_stack.
  Generate get return quadruple.

  Returns error if passed param quantity is different from the expected
  quantity.
  Returns error if param cannot be assigned.
  '''
  if not is_local:
    for instance in class_call_stack[-1]:
      generate_quadruple(Operations.ENTER_INSTANCE, instance,
                         None, instance.get_type())
  generate_quadruple(Operations.ERA, proc_call_stack[-1].class_name,
                     proc_call_stack[-1].func_name, None)

  generate_quadruple(Operations.SET_FOREIGN, None, None, None)

  func = (classes[proc_call_stack[-1].class_name]['#funcs']
                 [proc_call_stack[-1].func_name])
  expecting_params = func['#param_count']
  assigning_params = list(func['#vars'].values())
  if len(param_stack[-1]) != expecting_params:
    return (f"\'{func['#name']}\' expects {expecting_params}, but "
            + f'{len(param_stack[-1])} were given')
  count = 0
  for sending_param in param_stack[-1]:
    if not (semantic_cube[assigning_params[count]['#type']]
                         [sending_param.get_type()][Operations.EQUAL]):
      return f"Incompatible param #{count+1} on call to \'{func['#name']}\'"
    generate_quadruple(Operations.PARAM, sending_param, None,
                       assigning_params[count]['#address'])
    count += 1
  param_stack.pop()

  generate_quadruple(Operations.UNSET_FOREIGN, None, None, None)

  generate_quadruple(Operations.GOSUB, proc_call_stack[-1].class_name,
                     proc_call_stack[-1].func_name, None)

  if not is_local:
    while len(class_call_stack[-1]) > 0:
      generate_quadruple(Operations.EXIT_INSTANCE, None, None, None)
      class_call_stack[-1].pop()
  class_call_stack.pop()

  if proc_call_stack[-1].func_type in var_types:
    temp = build_temp_operand(proc_call_stack[-1].func_type)
    generate_quadruple(Operations.GET_RETURN, temp, None, None)
    operand_stack.append(temp)
    type_stack.append(temp.get_type())
  else:
    operand_stack.append(Types.VOID)
    type_stack.append(Types.VOID)
  proc_call_stack.pop()

  operator_stack.pop()


def add_arr_dim(dimension_size):
  if current_type not in var_types:
    return 'An array can store only primitive type_stack'
  if dimension_size < 1:
    return 'Size must be a positive integer'
  var = current_function['#vars'][last_declared_var]
  dim1 = {'#limsup': dimension_size - 1}
  global r
  r = dimension_size
  var['#dims'] = [dim1]


def add_arr_dim_2(dimension_size):
  if dimension_size < 1:
    return 'Size must be a positive integer'
  dims = current_function['#vars'][last_declared_var]['#dims']
  dimn = {'#limsup': dimension_size - 1}
  global r
  r *= dimension_size
  dims.append(dimn)


def arr_dim_complete():
  var = current_function['#vars'][last_declared_var]
  dims = var['#dims']
  global r
  address = var_avail.displace(current_type, r)
  if not address:
    return 'Not enough space.'
  var['#r'] = r
  for dim in dims:
    r //= dim['#limsup'] + 1
    dim['#m'] = r
  dims[-1]['#m'] = 0


def arr_access_2():
  id = operand_stack.pop().get_raw()
  type_stack.pop()
  if id in current_function['#vars']:
    var = current_function['#vars'][id]
  elif id in classes['#global']['#funcs']['#attributes']['#vars']:
    var = classes['#global']['#funcs']['#attributes']['#vars'][id]
  else:
    return f'Variable \'{id}\' does not exist'
  if '#dims' not in var:
    return f'Variable \'{id}\' has no dimensions'
  pila_dimensionada.append((var, 1))
  operator_stack.append(Operations.FAKE_BOTTOM)


def arr_access_3():
  var, dim = pila_dimensionada[-1]
  index = operand_stack[-1]
  if index.get_type() not in var_types != Types.POINTER:
    return 'Invalid type for index'
  generate_quadruple(Operations.VER, index, 0, var['#dims'][dim - 1]['#limsup'])
  if len(var['#dims']) > dim:
    aux = operand_stack.pop()
    type_stack.pop()
    t = build_temp_operand(Types.INT)
    generate_quadruple(Operations.TIMES, aux, get_or_create_cte_address(
        var['#dims'][dim - 1]['#m'], Types.INT), t)
    operand_stack.append(t)
    type_stack.append(t.get_type())
  if dim > 1:
    aux2 = operand_stack.pop()
    type_stack.pop()
    aux1 = operand_stack.pop()
    type_stack.pop()
    t = build_temp_operand(Types.INT)
    generate_quadruple(Operations.PLUS, aux1, aux2, t)
    operand_stack.append(t)
    type_stack.append(t.get_type())


def arr_access_4():
  var, dim = pila_dimensionada.pop()
  pila_dimensionada.append((var, dim + 1))


def arr_access_5():
  var, _ = pila_dimensionada.pop()
  aux = operand_stack.pop()
  t = build_temp_operand(Types.POINTER)
  generate_quadruple(Operations.PLUS, aux, get_or_create_cte_address(
      var['#address'], Types.INT), f'({t.get_raw()})')
  operand_stack.append(t)
  operator_stack.pop()


def generate_output():
  '''Generates object code to be read by the virtual machine.'''
  global classes

  constants = {}
  for values in constants_with_addresses.values():
    constants.update(invert_dict(values))

  # Clean symbol table for use in virtual machine.
  for clas in classes.values():
    del clas['#funcs']['#attributes']
    del clas['#parent']
    for func in clas['#funcs'].values():
      del func['#name']
      del func['#type']
      del func['#access']
      del func['#param_count']
      del func['#vars']

  return {
      'constants': constants,
      'quadruples': quadruples,
      'symbol_table': classes
  }
