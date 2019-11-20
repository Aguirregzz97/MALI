# Utils module for semantic checks and quadruples generation.

from implementation.utils.generic_utils import *  # pylint: disable=unused-wildcard-import
from implementation.utils.constants import *  # pylint: disable=unused-wildcard-import

# Symbol table utils.


def new_var_dict(var_type: Types, address: int, access=Access.PUBLIC,
                 assigned=False):
  '''Generates dictionary for a variable/attribute.

  This is meant to be added to the symbol table.
  '''

  var_dict = {
      '#assigned': assigned,
      '#type': var_type,
      '#address': address,
      '#access': access,
      '#inherited': False
  }
  return var_dict


def new_func_dict(name: str, func_type: Types):
  '''Generates dictionary for a function/method.

  This is meant to be added to the symbol table.
  '''

  func_dict = {
      '#name': name,
      '#type': func_type,
      '#access': Access.PUBLIC,
      '#param_count': 0,
      '#var_count': 0,
      '#vars': {}
  }
  return func_dict


def new_class_dict(name: str, parent='#global'):
  '''Generates dictionary for a class.

  This is meant to be added to the symbol table.
  '''

  class_dict = {
      '#name': name,
      '#parent': parent,
      '#funcs': {
          '#attributes': new_func_dict('#attributes', Types.VOID)
      }
  }
  return class_dict


class Available:
  '''Keeps track of the next available address.'''

  def __init__(self, begin: int, limit: int, types=avail_types):
    '''Takes an initial address, limit address, and types.

    Divides the available addresses into the received types.
    '''

    self.__begin = begin
    self.__limit = limit

    self.__type = {}
    type_begin = begin
    length = int((limit-begin)/len(types))
    for t in types:
      self.__type[t] = {
          'next': type_begin,
          'limit': (type_begin + length)
      }
      type_begin += length + 1

  def next(self, op_type: Types):
    '''Returns the next available address for a given type.'''

    if op_type not in self.__type:
      op_type = Types.CLASS

    next_val = self.__type[op_type]['next']
    if next_val > self.__type[op_type]['limit']:
      return None

    self.__type[op_type]['next'] += 1

    return next_val

  def displace(self, op_type, displace_size):
    '''Displaces the next available address for a given type.

    This is meant to be used by dimensionated variables.
    '''

    if op_type not in self.__type:
      op_type = Types.CLASS

    next_val = self.__type[op_type]['next'] + displace_size - 1
    if next_val > self.__type[op_type]['limit']:
      return None

    self.__type[op_type]['next'] += displace_size - 1
    return True


# Intermediate code generation utils

class Operand:
  '''Carries attributes of an Operand'''

  def __init__(self, raw=None):
    self.__raw = raw
    '''String name of the operand.'''

    self.__addr: int
    '''Address of the operand.'''

    self.__type: Types
    '''Type of the operand.'''

    self.__err = None
    '''Error that can be set when populating the operand.'''

  def set_raw(self, raw):
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


class FuncData:
  '''Carries attributes of a function.'''

  def __init__(self, func_name):
    self.func_name = func_name
    '''String with function name.'''

    self.class_name: str
    '''String with belonging class name.'''

    self.func_type: Types
    '''Return type of the function.'''

    self.error = None
    '''Error that can be set when populating the func.'''
