# Utils module for semantic checks and quadruples generation.

from implementation.utils.generic_utils import *  # pylint: disable=unused-wildcard-import
from implementation.utils.constants import *  # pylint: disable=unused-wildcard-import

# Symbol table utils.


def new_var_dict(var_type, address, access=Access.PUBLIC, assigned=False):
  var_dict = {
      '#assigned': assigned,
      '#type': var_type,
      '#address': address,
      '#access': access
  }
  return var_dict


def new_func_dict(name, func_type):
  func_dict = {
      '#name': name,
      '#type': func_type,
      '#access': Access.PUBLIC,
      '#param_count': 0,
      '#var_count': 0,
      '#vars': {}
  }
  return func_dict


def new_class_dict(name, parent='#global'):
  class_dict = {
      '#name': name,
      '#parent': parent,
      '#funcs': {
          '#attributes': new_func_dict('#attributes', Types.VOID)
      }
  }
  return class_dict


class Available:
  def __init__(self, begin, limit, types=avail_types):
    self.__begin = begin
    self.__limit = limit

    self.__type = {}
    type_begin = begin
    length = int((limit-begin)/len(types))
    for t in types:
      self.__type[t] = {
          # 'begin': type_begin,  # TODO: este podria no ser necesario.
          'next': type_begin,
          'limit': (type_begin + length)
      }
      type_begin += length + 1

  def next(self, op_type):
    if op_type not in self.__type:
      op_type = Types.CLASS

    next_val = self.__type[op_type]['next']
    if next_val > self.__type[op_type]['limit']:
      return None

    self.__type[op_type]['next'] += 1

    return next_val

  def displace(self, op_type, displace_size):
    if op_type not in self.__type:
      op_type = Types.CLASS

    next_val = self.__type[op_type]['next'] + displace_size - 1
    if next_val > self.__type[op_type]['limit']:
      return None

    self.__type[op_type]['next'] += displace_size - 1
    return True

# Intermediate code generation utils

class Operand:
  def __init__(self, raw=None):
    self.__raw = raw
    self.__addr = None
    self.__type = None
    self.__err = None

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
