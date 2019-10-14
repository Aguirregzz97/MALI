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
avail = available()


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
    elif raw_operand in classes[current_class][current_function]:
      type_or_error.val = (
          classes[current_class][current_function][raw_operand]['#type'])
      return False
  # TODO: VERIFICAR QUE ESTE DECLARADO EN SCOPE Y QUE ESTE ASIGNADO/INICIADO


def seenOperand(raw_operand):
  global operands, types
  type_or_error = val_or_error()
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


def generateQuadruple(operator):
  global operators, types, operands, quadruples, avail
  right_operand = operands.pop()
  right_type = types.pop()
  left_operand = operands.pop()
  left_type = types.pop()
  operator = operators.pop()
  result_type = sCube[left_type][right_type][operator]
  result = avail.next()
  quadruples.append([operator, left_operand, right_operand, result])
  operands.append(result)
  types.append(result_type)
  freeIfTemp(left_operand)
  freeIfTemp(right_operand)


def seenSubRule(ops):
  operator = top(operators)
  if operator in ops:
    generateQuadruple(operator)


def popFakeBottom():
  global operators
  operators.pop()


def assignment(result):
  global operators, types, operands, quadruples
  left_operand = operands.pop()
  left_type = types.pop()
  result_type_or_error = val_or_error()
  getType(result, result_type_or_error)
  if result_type_or_error.error:
    return type_or_error.error
  quadruples.append(['=', left_operand, None, result])
  operands.append(result)
  types.append(result_type_or_error.val)
