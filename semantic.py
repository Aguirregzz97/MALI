# Semantic vars.

current_class = 'global'
current_function = 'global'
current_access = 'public'


def new_var_dict(type=None, access=None):
  var_dict = {'id': None}
  if type: var_dict['type'] = type
  if access: var_dict['access'] = access
  return var_dict


def new_func_dict(type=None, access=None):
  func_dict = {}
  if type: func_dict['type'] = type
  if access: func_dict['access'] = access
  return func_dict


def new_class_dict(func, parent=None):
  return {'parent': parent, func: {}}


'''
def get_attr_table(class_name, method_name):
  return classes[class_name][method_name]


def get_methods_table(class_name):
  return classes[class_name]


def set_parent(class_name, parent):
  classes[class_name]
'''


classes = {'global': new_class_dict(func='global')}
types = {"int", "float", "char", "bool", "void"}

# Semantic checks.

def seenClass(class_name):
  if class_name in classes:
    return f"Repeated class name: {class_name}"
  else:
    global current_class
    current_class = class_name
    classes[class_name] = new_class_dict(func='attributes')
    types.add(class_name)


def classParent(class_parent):
  if class_parent not in classes:
    return f"Undeclared class parent: {class_parent}"
  else:
    classes[current_class]['parent'] = class_parent


def finishClass():
  global current_class, current_function
  current_class = 'global'
  current_function = 'global'


def seenAttr():
  global current_function
  current_function = 'attributes'
  classes[current_class][current_function] = new_func_dict()


def seenAccess(new_access):
  global current_access
  current_access = new_access

def seenType(new_type):
  if new_type not in types:
    return f"{new_type} is not a class nor data type"
  else:
    global current_type
    current_type = new_type


def varName(var_name):
  if var_name in classes[current_class][current_function]:
    return f"Redeclared variable: {var_name}"
  else:
    if current_class != 'global':
      classes[current_class][current_function][var_name] = (
          new_var_dict(type=current_type, access=current_access))
    else:
      classes[current_class][current_function][var_name] = (
          new_var_dict(type=current_type


