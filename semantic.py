# Semantic vars.

current_class = '#global'
current_function = '#attributes'
current_access = None
current_type = None
is_param = False
current_x = None
current_y = None


def new_var_dict(type=None, access=None):
  var_dict = {'#id': None}
  if type: var_dict['#type'] = type
  if access: var_dict['#access'] = access
  return var_dict


def new_func_dict(type=None, access=None):
  func_dict = {'#params': {}}
  if type: func_dict['#type'] = type
  if access: func_dict['#access'] = access
  return func_dict


def new_class_dict(parent=None):
  class_dict = {}
  if parent: class_dict['#parent'] = parent
  return class_dict


classes = {'#global': new_class_dict()}
classes['#global']['#attributes'] = new_func_dict()
types = {"int", "float", "char", "bool", "void"}

# Semantic checks.

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
  if new_type not in types and (
        new_type not in classes) or (
        new_type == '#global'):
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
    return f"{current_class} has no parent class but tries to extend \
        {parent} in constructor"
  elif parent not in classes[current_class]['#parent']:
    return f"{parent} is not {current_class}'s parent"


def isMethod():
  classes[current_class][current_function]['#access'] = current_access