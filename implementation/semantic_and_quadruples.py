from implementation.utils.semantic_and_quadruples_utils import *
from implementation.utils.generic_utils import *
from collections import defaultdict
import re

# Semantic table filling.

classes = {'#global': new_class_dict(name='#global', parent=None)}
possible_types = ("int", "float", "char", "bool", "void")

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
    global current_class
    classes[class_name] = new_class_dict(class_name)
    current_class = classes[class_name]


def classParent(class_parent):
  if class_parent not in classes:
    return f"Undeclared class parent: {class_parent}"
  else:
    current_class['#parent'] = class_parent


def finishClass():
  global current_class, current_function
  current_class = classes['#global']
  current_function = current_class['#funcs']['#attributes']


def seenFunc(func_name):
  global func_size
  func_size = 0
  if func_name in current_class['#funcs']:
    return f"Redeclared function {func_name}"
  else:
    global current_function
    current_class['#funcs'][func_name] = new_func_dict(func_name, current_type)
    current_function = current_class['#funcs'][func_name]


def seenAccess(new_access):
  global current_access
  current_access = new_access


def seenType(new_type):
  if new_type not in possible_types and (
        new_type not in classes):
    return f"{new_type} is not a class nor data type"
  else:
    global current_type
    current_type = new_type


def varName(var_name):
  if var_name in current_function['#vars']:
    return f"Redeclared variable: {var_name}"
  else:
    if is_param:
      global param_count
      param_count += 1
    else:
      global var_count
      var_count += 1
    if current_class['#name'] == '#global':
      current_function['#vars'][var_name] = new_var_dict(current_type)
    else:
      current_function['#vars'][var_name] = (
          new_var_dict(current_type, current_access))


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
quadruples = [['Goto', None, None, None]]
jumps = []
returns_count = 0
q_count = 1
temp_avail = available('#t')
calling_class = '#global'
calling_function = None
param_count = 0
var_count = 0


def generateQuadruple(a, b, c, d):
  global quadruples, q_count
  quadruples.append([a,b,c,d])
  q_count += 1


def findOperatorAndType(raw_operand, type_or_error, markAssigned=False):
  def search(prefix, checkAccess=False):
    nonlocal type_or_error
    prefix = prefix.get(raw_operand, None)
    if prefix:
      if markAssigned:
        prefix['#assigned'] = True
      elif not prefix['#assigned']:
        type_or_error.error = f'Variable {raw_operand} used before assignment'
      elif checkAccess and prefix.get('#access', 'public') == 'private':
        type_or_error.error = f'Variable {raw_operand} has private access'
      else:
        type_or_error.val = prefix['#type']
        return True
    return False

  if search(current_function['#vars']):
    return
  if search(current_class['#funcs']['#attributes']['#vars']):
    return
  curr_class = current_class['#parent']
  while curr_class:
    if search(classes[curr_class]['#funcs']['#attributes']['#vars'], True):
      return
    curr_class = classes[curr_class]['#parent']

  type_or_error.error = f'Variable {raw_operand} not in scope.'


# Assigns the type on type_or_error. If the variable does not exist,
# assigns error message to type_or_error. Returns boolean wether the
# operand is constant or not.
def getType(raw_operand, type_or_error):
  t = type(raw_operand)
  if t == int:
    type_or_error.val = 'int'
    return True
  elif t == float:
    type_or_error.val = 'float'
    return True
  elif t == bool:
    type_or_error.val = 'bool'
    return True
  elif t == str:
    if re.match(r"\'.\'", raw_operand):
      type_or_error.val = 'char'
      return True
    else:
      findOperatorAndType(raw_operand, type_or_error)
      return False


def seenOperand(raw_operand):
  global operands, types
  type_or_error = val_or_error()
  if type_or_error.error:
    return type_or_error.error
  isConstant = getType(raw_operand, type_or_error)
  if type_or_error.error:
    return type_or_error.error
  if isConstant:
    operands.append(raw_operand)
  else:
    operands.append(raw_operand)
  types.append(type_or_error.val)


def seenOperator(operator):
  global operators
  operators.append(str(operator))


def seenSubRule(ops):
  global operators, types, operands, temp_avail
  operator = top(operators)
  if operator in ops:
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    operator = operators.pop()
    result_type = sCube[left_type][right_type][operator]
    result = temp_avail.next()
    generateQuadruple(operator, left_operand, right_operand, result)
    operands.append(result)
    types.append(result_type)


def popFakeBottom():
  global operators
  operators.pop()


def doAssign(result):
  global operators, types, operands
  left_operand = operands.pop()
  left_type = types.pop()
  result_type_or_error = val_or_error()
  result_type_or_error = val_or_error()
  findOperatorAndType(result, result_type_or_error)
  if result_type_or_error.error: return result_type_or_error.error
  generateQuadruple('=', left_operand, None, result)
  types.append(result_type_or_error.val)


def doWrite(str):
  if str:
    generateQuadruple('write', None, None, str)
  else:
    word = operands.pop()
    type = types.pop()
    word_type_or_error = val_or_error()
    getType(word, word_type_or_error)
    if word_type_or_error.error: return word_type_or_error.error
    generateQuadruple('write', None, None, word)


def doRead():
  global operands
  operands.append('#read')


def seenCondition():
  exp_type = types.pop()
  if exp_type != 'bool':
    return 'Evaluated expression is not boolean'
  result = operands.pop()
  generateQuadruple('GotoF', result, None, None)
  jumps.append(q_count-1)


def seenElse():
  generateQuadruple('Goto', None, None, None)
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
  generateQuadruple('Goto', None, None, ret)


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
    generateQuadruple('END', None, None, None)
  else:
    generateQuadruple('ENDPROC', None, None, None)


def seenReturn():
  global returns_count
  function_type = current_function['#type']
  if function_type == 'void':
    return 'Void function cannot return a value'
  return_val = operands.pop()
  return_type = types.pop()
  if function_type != return_type:
    return f'Cannot return type {return_type} as {function_type}'
  generateQuadruple('RETURN', return_val, None, None)
  jumps.append(q_count)
  returns_count += 1
  generateQuadruple('Goto', None, None, None)


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
  generateQuadruple('ERA', calling_function['#name'], size, None)


def passParam():
  param = list(calling_function['#vars'].values())[param_count]
  param_type = param['#type']
  argument = operands.pop()
  arg_type = types.pop()
  if param_type != arg_type:
    return (f"{calling_function['#name']} expecting type {param_type} "
        + f'for parameter {param_count+1}')
  generateQuadruple('param', argument, None, 'param'+str(param_count))


def nextPassParam():
  global param_count
  param_count += 1


def doneParamPass():
  expected = calling_function['#var_count']
  if param_count+1 != expected:
    return (f'{calling_function} expects {expected} parameters, but ' +
        f'{param_count+1} were given')
  generateQuadruple('GOSUB', calling_function['#name'], None,
                    calling_function['#start'])