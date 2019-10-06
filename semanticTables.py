# Semantic vars.

current_class = 'global'
current_function = 'global'
current_access = 'public'

var_dict = {'id': None, 'access': None}
function_dict = {'type': None, 'global': var_dict}
class_dict = {'parent': None, 'global': function_dict}

variables = { }
functions = {'global': function_dict}
classes = {'global': class_dict}

# TODO: modificar para que solo se incluya access en el diccionario si se 
# especifica.
def new_var_dict(id=None, type=None, access=None):
  return {'id': id, 'type': type, 'access': access}

# TODO: modificar para que solo se incluya access en el diccionario si se 
# especifica.
def new_func_dict(name='global', type=None, access=None):
  return {'type': type, name: {}, 'access': access}


def new_class_dict(parent=None):
  return {'parent': parent, 'global': {}}

'''
def get_attr_table(class_name, method_name):
  return classes[class_name][method_name]


def get_methods_table(class_name):
  return classes[class_name]


def set_parent(class_name, parent):
  classes[class_name]
'''