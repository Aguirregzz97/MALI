# Utils module for semantic checks and quadruples generation.

from implementation.utils.generic_utils import *
from implementation.utils.constants import *

# Symbol table utils.

def new_var_dict(type, address, access=None):
  var_dict = {
    #TODO: hacer verdadero.
    '#assigned': True,
    '#type': type,
    '#address': address
  }
  if access: var_dict['#access'] = access
  return var_dict


def new_func_dict(name, type):
  func_dict = {
    '#name': name,
    '#type': type,
    '#param_count': 0,
    '#var_count': 0,
    '#var_avail': Available(VAR_LOWER_LIMIT, VAR_UPPER_LIMIT, var_types),
    '#temp_avail': Available(TEMP_LOWER_LIMIT, TEMP_UPPER_LIMIT, temp_types),
    '#vars': {}
  }
  return func_dict


def new_class_dict(name, parent='#global'):
  class_dict = {
    '#name': name,
    '#parent': parent,
    '#funcs': {
      '#attributes': new_func_dict('#attributes', 'void')
    }
  }
  return class_dict


var_types = ("int", "float", "char", "bool", "class")
temp_types = ("int", "float", "char", "bool")
const_types = ("int", "float", "char", "bool", "cte_string")
func_types = ("int", "float", "char", "bool", "void")


class Available:
  def __init__(self, begin, limit, types):
    self.__begin = begin
    self.__limit = limit

    self.__type = {}
    type_begin = begin
    length = int((limit-begin)/len(types))
    for t in types:
      self.__type[t] = {
        'begin': type_begin, #TODO: este podria no ser necesario.
        'next': type_begin,
        'limit': (type_begin + length)
      }
      type_begin += length + 1

  def next(self, type):
    if type not in self.__type:
      type = "class"

    next_val = self.__type[type]['next']
    if next_val > self.__type[type]['limit']:
      return None

    self.__type[type]['next'] += 1

    return next_val


# Intermediate code generation utils

class Operand:
  def __init__(self, raw=None):
    self.__raw = raw
    self.__addr = None
    self.__type = None
    self.__err = None

  def set_raw(self, raw):
    if (self.__raw):
      raise Exception('raw can only be defined once')
    self.__raw = raw

  def set_address(self, addr):
    self.__addr = addr

  def set_type(self, type):
    self.__type = type

  def set_error(self, err):
    self.__err = err

  def get_raw(self): return self.__raw
  def get_address(self): return self.__addr
  def get_type(self): return self.__type
  def get_error(self): return self.__err


def address_or_else(operand, is_visual=False):
  if operand:
    if isinstance(operand, Operand):
      if is_visual:
        return operand.get_raw()
      else:
        return operand.get_address()
    else:
      return operand
  return None


def populate_non_constant_operand_aux(operand, prefix, mark_assigned,
                                      check_access=False):
  raw_operand = operand.get_raw()
  var = prefix.get(raw_operand, None)
  if not var:
    return False
  if mark_assigned:
    var['#assigned'] = True
  if not var['#assigned']:
    operand.set_error(f'Variable {raw_operand} used before assignment')
  elif check_access and var.get('#access', 'public') == 'private':
    operand.set_error(f'Variable {raw_operand} has private access')
  else:
    operand.set_type(var['#type'])
    operand.set_address(var['#address'])
    return True