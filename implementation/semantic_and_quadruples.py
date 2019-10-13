from implementation.utils.semantic_and_quadruples_utils import *

# Semantic table filling.

current_class = '#global'
current_function = '#attributes'
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
  if '#parent' not in classes[current_class]:
    return f'{current_class} has no parent class but tries to extend ' + (
        f'{parent} in constructor')
  elif parent not in classes[current_class]['#parent']:
    return f"{parent} is not {current_class}'s parent"


def isMethod():
  classes[current_class][current_function]['#access'] = current_access


# Intermediate code generation.

operators = []
types = []
operands = []
quadruples = []
next_temp = 1

def getOperand(rawOperand):
  pass

def seenOperand(operand):
  global operands, types
  if isinstance(operand, tuple):
    operand = top(operand)
  if operand in classes[current_class][current_function]:
    opType = classes[current_class][current_function][operand]['#type']
  else:
    opType = type(operand)
  operands.append(operand)
  types.append(opType)

def seenOperator(operator):
  global operators
  operators.append(str(operator))

def seenSubRule(ops):
  global operators, types, operands, quadruples, next_temp
  operator = top(operators)
  if operator in ops:
    right_operand = operands.pop()
    right_type = types.pop()
    left_operand = operands.pop()
    left_type = types.pop()
    operator = operators.pop()
    result_type = sCube[left_type][right_type][operator]
    result = '#t' + str(next_temp)
    quadruples.append([operator, left_operand, right_operand, result])
    operands.append(result)
    types.append(result_type)
    next_temp += 1
