# Semantic vars.

current_class = 'global'
current_function = 'global'
current_access = 'public'
in_class = False

var_dict = {'id': None, 'access': None}
function_dict = {'type': None, 'global': var_dict}
class_dict = {'parent': None, 'global': function_dict}

variables = { }
functions = {'global': function_dict}
classes = {'global': class_dict}


def new_attr_dict(id=None, type=None, access=None):
  return {'id': id, 'type': None, 'access': access}


def new_methods_dict(type=None, access=None):
  return {'type': type, 'global': {}, 'access': access}


def new_class_dict(parent=None):
  return {'parent': parent, 'global': {}}


def get_attr_table(class_name, method_name):
  return classes[class_name][method_name]


def get_methods_table(class_name):
  return classes[class_name]


def set_parent(class_name, parent):
  classes[class_name]