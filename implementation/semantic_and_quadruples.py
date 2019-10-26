from implementation.utils.semantic_and_quadruples_utils import *
from implementation.utils.generic_utils import *
from collections import defaultdict
import re

# Semantic table filling.

classes = {'#global': new_class_dict()}
possible_types = ("int", "float", "char", "bool", "void")

current_class = '#global'
current_function = '#attributes'
current_access = None
current_type = None
is_param = False
current_x = None
current_y = None
param_counter = 0
var_counter = 0

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


def exists_variable(var_name):
  return var_name in classes[current_class]['#funcs'][current_function]


def varName(var_name):
  if exists_variable(var_name):
    return f"Redeclared variable: {var_name}"
  else:
    if is_param:
      global param_counter
      param_counter += 1
    else:
      global var_counter
      var_counter += 1
    if current_class != '#global':
      classes[current_class]['#funcs'][current_function]['#vars'][var_name] = (
          new_var_dict(type=current_type, access=current_access))
    else:
      classes[current_class]['#funcs'][current_function]['#vars'][var_name] = (
          new_var_dict(type=current_type))


def setParam(val):
  global param_counter
  if val:
    param_counter = 0
  else:
    classes[current_class]['#funcs'][current_function]['#param_counter'] = (
        param_counter)
  global is_param
  is_param = val


def callParent(parent):
  if not classes[current_class]['#parent']:
    return f'{current_class} has no parent class but tries to extend ' + (
        f'{parent} in constructor')
  elif parent != classes[current_class]['#parent']:
    return f"{parent} is not {current_class}'s parent"


def isMethod():
  classes[current_class]['#funcs'][current_function]['#access'] = current_access


# Intermediate code generation.

operators = []
types = []
operands = []
quadruples = [['Goto', None, None, None]]
jumps = []
returnsCount = 0
qCount = 1
avail = available()


def generateQuadruple(a, b, c, d):
  global quadruples, qCount
  quadruples.append([a,b,c,d])
  qCount += 1


def findOperatorAndType(raw_operand, type_or_error, markAssigned=False):
  def search(prefix, checkAccess=False):
    nonlocal type_or_error
    prefix = prefix.get(raw_operand, None)
    if prefix:
      if markAssigned:
        prefix['#assigned'] = True
      elif not prefix['#assigned']:
        type_or_error.error = f'Variable {raw_operand} not yet assigned'
      elif checkAccess and prefix.get('#access', 'public') == 'private':
        type_or_error.error = f'Variable {raw_operand} has private access'
      else:
        type_or_error.val = prefix['#type']
        return True
    return False

  if not search(classes[current_class]['#funcs'][current_function]['#vars']):
    if not search(classes[current_class]['#funcs']['#attributes']['#vars']):
      curr_class = current_class
      while True:
        curr_class = classes[curr_class]['#parent']
        if (search(classes[curr_class]['#funcs']['#attributes']['#vars'], True)
            or curr_class == '#global'):
          break
        else:
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
    findOperatorAndType(word, word_type_or_error)
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
  jumps.append(qCount-1)


def seenElse():
  generateQuadruple('Goto', None, None, None)
  false = jumps.pop()
  jumps.append(qCount-1)
  quadruples[false][3] = qCount


def seenEndIf():
  end = jumps.pop()
  quadruples[end][3] = qCount


def seenWhile():
  jumps.append(qCount)


def seenEndWhile():
  end = jumps.pop()
  quadruples[end][3] = qCount
  ret = jumps.pop()
  generateQuadruple('Goto', None, None, ret)


def endVars():
  global var_counter
  classes[current_class]['#funcs'][current_function]['#var_counter'] = var_counter
  var_counter = 0


def startFunc():
  classes[current_class]['#funcs'][current_function]['#start'] = qCount


def setVoid():
  global current_type
  current_type = 'void'


def seenMain():
  quadruples[0][3] = qCount


def finishFunc(is_main=False):
  global returnsCount
  while returnsCount:
    quadruples[jumps.pop()][3] = qCount
    returnsCount -= 1
  if is_main:
    generateQuadruple('END', None, None, None)
  else:
    generateQuadruple('ENDPROC', None, None, None)


def seenReturn():
  global returnsCount
  function_type = classes[current_class]['#funcs'][current_function]['#type']
  if function_type == 'void':
    return 'Void function cannot return a value'
  return_val = operands.pop()
  return_type = types.pop()
  if function_type != return_type:
    return f'Cannot return type {return_type} as {function_type}'
  generateQuadruple('RETURN', return_val, None, None)
  jumps.append(qCount)
  returnsCount += 1
  generateQuadruple('Goto', None, None, None)


def seenCall(func_name):
  if func_name in classes[current_class]['#funcs']:
    return
  while True:
    curr_class = classes[current_class]['#parent']
    if func_name in classes[curr_class]['#funcs']:
      return
    if curr_class == '#global': break;
  return f'{func_name} not defined for {current_class}'