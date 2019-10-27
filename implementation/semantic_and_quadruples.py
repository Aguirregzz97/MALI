from implementation.utils.semantic_and_quadruples_utils import *
from implementation.utils.generic_utils import *
from collections import defaultdict
import re

# Semantic table filling.

classes = {'#global': new_class_dict(parent=None)}
possible_types = ("int", "float", "char", "bool", "void")

current_class = '#global'
current_function = '#attributes'
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
    current_class = class_name
    classes[class_name] = new_class_dict()


def classParent(class_parent):
  if class_parent not in classes:
    return f"Undeclared class parent: {class_parent}"
  else:
    classes[current_class]['#parent'] = class_parent


def finishClass():
  global current_class, current_function
  current_class = '#global'
  current_function = '#attributes'


def seenFunc(new_function):
  global func_size
  func_size = 0
  if new_function in classes[current_class]['#funcs']:
    return f"Redeclared function {new_function}"
  else:
    global current_function
    current_function = new_function
    classes[current_class]['#funcs'][current_function] = new_func_dict(
        type=current_type)


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
  if var_name in classes[current_class]['#funcs'][current_function]:
    return f"Redeclared variable: {var_name}"
  else:
    if is_param:
      global param_count
      param_count += 1
    else:
      global var_count
      var_count += 1
    if current_class == '#global':
      classes[current_class]['#funcs'][current_function]['#vars'][var_name] = (
          new_var_dict(type=current_type, access='public'))
    else:
      classes[current_class]['#funcs'][current_function]['#vars'][var_name] = (
          new_var_dict(type=current_type, access=current_access))


def setParam(val):
  global param_count
  if val:
    param_count = 0
  else:
    classes[current_class]['#funcs'][current_function]['#param_count'] = (
        param_count)
  global is_param
  is_param = val


def isMethod():
  classes[current_class]['#funcs'][current_function]['#access'] = current_access


# Intermediate code generation.

operators = []
types = []
operands = []
quadruples = [['Goto', None, None, None]]
jumps = []
returns_count = 0
q_count = 1
avail = available()
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

  if search(classes[current_class]['#funcs'][current_function]['#vars']):
    return
  if search(classes[current_class]['#funcs']['#attributes']['#vars']):
    return
  curr_class = classes[current_class]['#parent']
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


def freeIfTemp(operand):
  if re.match(r"[t].*", str(operand)):
    avail.free(operand)


def seenSubRule(ops):
  global operators, types, operands, avail
  operator = top(operators)
  if operator in ops:
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    operator = operators.pop()
    result_type = sCube[left_type][right_type][operator]
    result = avail.next()
    generateQuadruple(operator, left_operand, right_operand, result)
    operands.append(result)
    types.append(result_type)
    freeIfTemp(left_operand)
    freeIfTemp(right_operand)


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
  classes[current_class]['#funcs'][current_function]['#var_count'] = var_count
  var_count = 0


def startFunc():
  classes[current_class]['#funcs'][current_function]['#start'] = q_count


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
  function_type = classes[current_class]['#funcs'][current_function]['#type']
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
  if not classes[current_class]['#parent']:
    return f'{current_class} has no parent class but tries to extend ' + (
        f'{parent} in constructor')
  elif parent != classes[current_class]['#parent']:
    return f"{parent} is not {current_class}'s parent"
  calling_class = parent
  calling_function = 'init'

def seenCall(func_name):
  print(func_name)
  global calling_class, calling_function
  calling_function = func_name
  if func_name in classes[current_class]['#funcs']:
    calling_class = current_class
    return
  curr_class = classes[current_class]['#parent']
  while curr_class:
    if func_name in classes[curr_class]['#funcs']:
      calling_class = current_class
      return
    curr_class = classes[curr_class]['#parent']
  return f'{func_name} not defined for {current_class}'


def startParams():
  global param_count
  param_count = 0
  function = classes[calling_class]['#funcs'][calling_function]
  size = function['#param_count'] + function['#var_count']
  generateQuadruple('ERA', calling_function, size, None)

def passParam():
  param = list(classes[calling_class]['#funcs'][calling_function]['#vars'].values())[param_count]
  print(param)
  param_type = param['#type']
  argument = operands.pop()
  arg_type = types.pop()
  if param_type != arg_type:
    return f'{calling_function} expecting type {param_type} for parameter {param_count+1}'
  generateQuadruple('param', argument, None, 'param'+str(param_count))

def nextPassParam():
  global param_count
  param_count += 1

def doneParamPass():
  expected = classes[calling_class]['#funcs'][calling_function]['#var_count']
  if param_count+1 != expected:
    return f'{calling_function} expects {expected} parameters, but {param_count+1} were given'
  ret = classes[calling_class]['#funcs'][calling_function]['#start']
  generateQuadruple('GOSUB', calling_function, None, ret)