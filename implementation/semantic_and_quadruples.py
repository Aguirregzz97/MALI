from implementation.utils.semantic_and_quadruples_utils import *
from implementation.utils.generic_utils import *
from implementation.utils.constants import *
from collections import defaultdict
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


def seenClass(class_name):
  if class_name in classes:
    return f"Repeated class name: {class_name}"
  else:
    global current_class, current_function
    classes[class_name] = new_class_dict(class_name)
    current_class = classes[class_name]
    current_function = current_class['#funcs']['#attributes']


def classParent(class_parent):
  if class_parent not in classes:
    return f"Undeclared class parent: {class_parent}"
  else:
    current_class['#parent'] = class_parent


def finishClass():
  global current_class, current_function
  current_class = classes['#global']
  current_function = current_class['#funcs']['#attributes']
  current_access = '#public'


def seenFunc(func_name):
  global func_size, current_function
  func_size = 0
  if func_name in current_class['#funcs']:
    return f"Redeclared function {func_name}"
  else:
    current_class['#funcs'][func_name] = new_func_dict(func_name, current_type)
    current_function = current_class['#funcs'][func_name]


def seenAccess(new_access):
  global current_access
  current_access = new_access


def seenType(new_type):
  if new_type not in func_types and (
        new_type not in classes):
    return f"{new_type} is not a class nor data type"
  else:
    global current_type
    current_type = new_type


def varName(var_name):
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


def setParam(val):
  global param_count, is_param
  if val:
    param_count = 0
  else:
    current_function['#param_count'] = param_count
  is_param = val


def isMethod():
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
calling_class = None
calling_function = None
param_count = 0
var_count = 0


def addressOrElse(operand):
  if operand:
    if isinstance(operand, Operand):
      return operand.get_address()
    else:
      return operand
  return None

def nameOrElse(operand):
  if operand:
    if isinstance(operand, Operand):
      return operand.get_raw()
    else:
      return operand
  return None

def generateQuadruple(a, b, c, d):
  global quadruples, q_count

  operation = operations.get(a, f'NOT FOUND {a}')
  left_operand = addressOrElse(b)
  right_operand = addressOrElse(c)
  result = addressOrElse(d)

  quadruples.append([operation, left_operand, right_operand, result])
  q_count += 1

  v_left_operand = nameOrElse(b)
  v_right_operand = nameOrElse(c)
  v_result = nameOrElse(d)
  visual_quadruples.append([a, v_left_operand, v_right_operand, v_result])


def populateNonConstantOperand(operand, mark_assigned=False):
  if populateNonConstantOperandAux(operand, current_function['#vars'],
                                   mark_assigned):
    return
  if populateNonConstantOperandAux(operand,
      current_class['#funcs']['#attributes']['#vars'], mark_assigned):
    return
  curr_class = current_class['#parent']
  while curr_class:
    if populateNonConstantOperandAux(operand,
        classes[curr_class]['#funcs']['#attributes']['#vars'],
        mark_assigned,
        True):
      return
    curr_class = classes[curr_class]['#parent']

  if not operand.get_error():
    operand.set_error(f'Variable {operand.get_raw()} not in scope.')


def buildOperand(raw_operand):
  t = type(raw_operand)
  operand = Operand(raw_operand)
  if t == int:
    operand.set_type('int')
    operand.set_address(const_avail.next('int'))
  elif t == float:
    operand.set_type('float')
    operand.set_address(const_avail.next('float'))
  elif t == bool:
    operand.set_type('bool')
    operand.set_address(const_avail.next('bool'))
  elif t == str:
    if re.match(r"\'.\'", raw_operand):
      operand.set_type('char')
      operand.set_address(const_avail.next('char'))
    else:
      populateNonConstantOperand(operand)
  return operand


def seenOperand(raw_operand):
  global operands, types
  operand = buildOperand(raw_operand)
  if operand.get_error(): return operand.get_error()
  operands.append(operand)
  types.append(operand.get_type())


def seenOperator(operator):
  global operators
  operators.append(str(operator))


def buildTempOperand(op_type):
  address = current_function['#temp_avail'].next(op_type)
  current_function['#vars'][address] = new_var_dict(type, address)
  current_function['#var_count'] += 1
  operand = Operand()
  operand.set_address(address)
  operand.set_type(type)
  return operand


def seenSubRule(ops):
  global operators, types, operands
  operator = top(operators)
  if operator in ops:
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    operator = operators.pop()
    result_type = sCube[left_type][right_type][operator]
    if not result_type:
      return (f'Type mismatch: Invalid operation {operator} on given operands')
    temp = buildTempOperand(result_type)
    generateQuadruple(operator, left_operand, right_operand, temp)
    operands.append(temp)
    types.append(result_type)


def popFakeBottom():
  global operators
  operators.pop()


def doAssign(result):
  global operators, types, operands
  left_operand = operands.pop()
  left_type = types.pop()
  result_operand = Operand(result)
  populateNonConstantOperand(result_operand, True)
  if result_operand.get_error(): return result_operand.get_error()
  result_type = result_operand.get_type()
  if not sCube[result_type][left_type]['=']:
    return (f'Type mismatch: expression cannot be assigned to {result}')
  generateQuadruple('=', left_operand, None, result_operand)
  types.append(result_type)


def doWrite(s):
  if s:
    operand = Operand(s)
    operand.set_type('cte_string')
    operand.set_address(const_avail.next('cte_string'))
    generateQuadruple('write', None, None, operand)
  else:
    word = operands.pop()
    type = types.pop()
    operand = buildOperand(word)
    if operand.get_error(): return operand.get_error()
    generateQuadruple('write', None, None, word)


def doRead():
  global operands, types
  operand = Operand('read')
  operand.set_address(operations['read'])
  operand.set_type('dynamic')
  operands.append(operand)
  types.append('dynamic')


def seenCondition():
  exp_type = types.pop()
  if exp_type != 'bool':
    return 'Evaluated expression is not boolean'
  result = operands.pop()
  generateQuadruple('gotof', result, None, None)
  jumps.append(q_count-1)


def seenElse():
  generateQuadruple('goto', None, None, None)
  false = jumps.pop()
  jumps.append(q_count-1)
  quadruples[false][3] = q_count


def seenEndIf():
  end = jumps.pop()
  quadruples[end][3] = q_count


def seenWhile():
  jumps.append(q_count)


def seenEndWhile():
  end = jumps.pop()
  quadruples[end][3] = q_count
  ret = jumps.pop()
  generateQuadruple('goto', None, None, ret)


def endVars():
  global var_count
  current_function['#var_count'] = var_count
  var_count = 0


def startFunc():
  current_function['#start'] = q_count


def setVoid():
  global current_type
  current_type = 'void'


def seenMain():
  quadruples[0][3] = q_count


def finishFunc(is_main=False):
  global returns_count
  while returns_count:
    quadruples[jumps.pop()][3] = q_count
    returns_count -= 1
  if is_main:
    generateQuadruple('end', None, None, None)
  else:
    generateQuadruple('endproc', None, None, None)


def seenReturn():
  global returns_count
  function_type = current_function['#type']
  if function_type == 'void':
    return 'Void function cannot return a value'
  return_val = operands.pop()
  return_type = types.pop()
  if function_type != return_type:
    return f'Cannot return type {return_type} as {function_type}'
  generateQuadruple('return', return_val, None, None)
  jumps.append(q_count)
  returns_count += 1
  generateQuadruple('goto', None, None, None)


def callParent(parent):
  global calling_class, calling_function
  if not current_class['#parent']:
    return (f"{current_class['#name']} has no parent class but tries "
        + f'to extend {parent} in constructor')
  elif parent != current_class['#parent']:
    return f"{parent} is not {current_class['#name']}'s parent"
  calling_class = classes[parent]
  calling_function = calling_class['#funcs']['init']


def seenCall(func_name):
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


def startParams():
  global param_count
  param_count = 0
  size = calling_function['#param_count'] + calling_function['#var_count']
  generateQuadruple('era', calling_function['#name'], size, None)


def passParam():
  param = list(calling_function['#vars'].values())[param_count]
  param_type = param['#type']
  argument = operands.pop()
  arg_type = types.pop()
  if param_type != arg_type:
    return (f"{calling_function['#name']} expecting type {param_type} "
        + f'for parameter {param_count+1}')
  #TODO: en el ejemplo param se imprime enel cuadruplo como 'param#'
  generateQuadruple('param', argument, None, param_count)


def paramPassError():
  expected = calling_function['#var_count']
  return (f'{calling_function} expects {expected} parameters, but ' +
        f'{param_count+1} were given')


def nextPassParam():
  global param_count
  param_count += 1
  if param_count+1 > calling_function['#var_count']:
    expected = calling_function['#var_count']
    return (f'{calling_function} expects {expected} parameters, but more' +
        'were given')


def doneParamPass():
  expected = calling_function['#var_count']
  if param_count+1 != expected:
    return (f'{calling_function} expects {expected} parameters, but ' +
        f'{param_count+1} were given')
  generateQuadruple('gosub', calling_function['#name'], None,
                    calling_function['#start'])