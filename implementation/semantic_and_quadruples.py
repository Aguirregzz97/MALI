from implementation.utils.semantic_and_quadruples_utils import *
from implementation.utils.generic_utils import *
from collections import defaultdict
import re

# Semantic table filling.

current_class = '#global'
current_function = '#attributes'
current_instance = ''
current_access = None
current_type = None
is_param = False
current_x = None
current_y = None

classes = {'#global': new_class_dict()}
classes['#global']['#attributes'] = new_func_dict()
possible_types = ("int", "float", "char", "bool", "void")

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


def seenFunc(new_function, recordType=False):
  if new_function in classes[current_class]:
    return f"Redeclared function {new_function}"
  else:
    global current_function
    current_function = new_function
    if recordType:
      classes[current_class][current_function] = new_func_dict(
          type=current_type)
    else:
      classes[current_class][current_function] = new_func_dict()


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
  return var_name in classes[current_class][current_function]['#params'] or (
      var_name in classes[current_class][current_function])


def varName(var_name):
  if exists_variable(var_name):
    return f"Redeclared variable: {var_name}"
  else:
    if is_param:
      classes[current_class][current_function]['#params'][var_name] = (
          new_var_dict(type=current_type))
    elif current_class != '#global':
      classes[current_class][current_function][var_name] = (
          new_var_dict(type=current_type, access=current_access))
    else:
      classes[current_class][current_function][var_name] = (
          new_var_dict(type=current_type))


def setParam(val):
  global is_param
  is_param = val


def callParent(parent):
  if not classes[current_class]['#parent']:
    return f'{current_class} has no parent class but tries to extend ' + (
        f'{parent} in constructor')
  elif parent != classes[current_class]['#parent']:
    return f"{parent} is not {current_class}'s parent"


def isMethod():
  classes[current_class][current_function]['#access'] = current_access


# Intermediate code generation.

operators = []
types = []
operands = []
quadruples = []
jumps = []
qCount = 0
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
      if not prefix['#assigned']:
        type_or_error.error = f'Variable {raw_operand} not yet assigned'
      elif checkAccess and prefix.get('#access', 'public') == 'private':
        type_or_error.error = f'Variable {raw_operand} has private access'
      else:
        type_or_error.val = prefix['#type']
        return True
    return False

  if not search(classes[current_class][current_function]['#params']):
    if not search(classes[current_class][current_function]):
      if not search(classes[current_class]['#attributes']):
        curr_class = current_class
        while True:
          curr_class = classes[curr_class]['#parent']
          if search(classes[curr_class]['#attributes'], True) or (
              curr_class == '#global'):
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
    operands.append(f'{current_instance}{raw_operand}')
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
