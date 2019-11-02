from collections import defaultdict, deque
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


def populateNonConstantOperandAux(operand, prefix, mark_assigned,
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


operations = {
  1: '+unary',
  2: '-unary',
  3: 'not',
  4: '*',
  5: '/',
  6: '+',
  7: '-',
  8: '>',
  9: '<',
  10: '<>',
  11: '==',
  12: '<=',
  13: '>=',
  14: 'or',
  15: 'and',
  16: '=',
  17: 'read',
  18: 'write',
  19: 'goto',
  20: 'gotof',
  21: 'gosub',
  22: 'param',
  23: 'era',
  24: 'return',
  25: 'endproc',
  26: 'end',

  '+unary': 1,
  '-unary': 2,
  'not': 3,
  '*': 4,
  '/': 5,
  '+': 6,
  '-': 7,
  '>': 8,
  '<': 9,
  '<>': 10,
  '==': 11,
  '<=': 12,
  '>=': 13,
  'or': 14,
  'and': 15,
  '=': 16,
  'read': 17,
  'write': 18,
  'goto': 19,
  'gotof': 20,
  'gosub': 21,
  'param': 22,
  'era': 23,
  'return': 24,
  'endproc': 25,
  'end': 26
}


sCube = defaultdict(lambda : defaultdict(lambda : defaultdict(
    lambda : defaultdict(None))))

sCube['int']['int']['and'] = 'bool'
sCube['int']['int']['or'] = 'bool'
sCube['int']['int']['>'] = 'bool'
sCube['int']['int']['<'] = 'bool'
sCube['int']['int']['<>'] = 'bool'
sCube['int']['int']['=='] = 'bool'
sCube['int']['int']['<='] = 'bool'
sCube['int']['int']['>='] = 'bool'
sCube['int']['int']['+'] = 'int'
sCube['int']['int']['-'] = 'int'
sCube['int']['int']['*'] = 'int'
sCube['int']['int']['/'] = 'int'
sCube['int']['int']['='] = 'int'
sCube['int']['dynamic']['='] = 'int'

sCube['float']['float']['and'] = 'bool'
sCube['float']['float']['or'] = 'bool'
sCube['float']['float']['>'] = 'bool'
sCube['float']['float']['<'] = 'bool'
sCube['float']['float']['<>'] = 'bool'
sCube['float']['float']['=='] = 'bool'
sCube['float']['float']['<='] = 'bool'
sCube['float']['float']['>='] = 'bool'
sCube['float']['float']['+'] = 'float'
sCube['float']['float']['-'] = 'float'
sCube['float']['float']['*'] = 'float'
sCube['float']['float']['/'] = 'float'
sCube['float']['float']['='] = 'float'
sCube['float']['dynamic']['='] = 'float'

sCube['char']['char']['and'] = 'bool'
sCube['char']['char']['or'] = 'bool'
sCube['char']['char']['>'] = 'bool'
sCube['char']['char']['<'] = 'bool'
sCube['char']['char']['<>'] = 'bool'
sCube['char']['char']['=='] = 'bool'
sCube['char']['char']['>='] = 'bool'
sCube['char']['char']['<='] = 'bool'
sCube['char']['char']['+'] = 'char'
sCube['char']['char']['-'] = 'char'
sCube['char']['char']['*'] = 'char'
sCube['char']['char']['/'] = 'char'
sCube['char']['char']['='] = 'char'
sCube['char']['dynamic']['='] = 'char'

sCube['bool']['bool']['and'] = 'bool'
sCube['bool']['bool']['or'] = 'bool'
sCube['bool']['bool']['>'] = 'bool'
sCube['bool']['bool']['<'] = 'bool'
sCube['bool']['bool']['<>'] = 'bool'
sCube['bool']['bool']['=='] = 'bool'
sCube['bool']['bool']['>='] = 'bool'
sCube['bool']['bool']['<='] = 'bool'
sCube['bool']['bool']['+'] = 'int'
sCube['bool']['bool']['-'] = 'int'
sCube['bool']['bool']['*'] = 'int'
sCube['bool']['bool']['/'] = 'int'
sCube['bool']['bool']['='] = 'bool'
sCube['bool']['dynamic']['='] = 'bool'

sCube['int']['float']['and'] = sCube['float']['int']['and'] = 'bool'
sCube['int']['float']['or'] = sCube['float']['int']['or'] = 'bool'
sCube['int']['float']['>'] = sCube['float']['int']['>'] = 'bool'
sCube['int']['float']['<'] = sCube['float']['int']['<'] = 'bool'
sCube['int']['float']['<>'] = sCube['float']['int']['<>'] = 'bool'
sCube['int']['float']['=='] = sCube['float']['int']['=='] = 'bool'
sCube['int']['float']['<='] = sCube['float']['int']['<='] = 'bool'
sCube['int']['float']['>='] = sCube['float']['int']['>='] = 'bool'
sCube['int']['float']['+'] = sCube['float']['int']['+'] = 'float'
sCube['int']['float']['-'] = sCube['float']['int']['-'] = 'float'
sCube['int']['float']['*'] = sCube['float']['int']['*'] = 'float'
sCube['int']['float']['/'] = sCube['float']['int']['/'] = 'float'
sCube['int']['float']['='] = 'int'
sCube['float']['int']['='] = 'float'

sCube['int']['char']['and'] = sCube['char']['int']['and'] = 'char'
sCube['int']['char']['or'] = sCube['char']['int']['or'] = 'char'
sCube['int']['char']['>'] = sCube['char']['int']['>'] = 'char'
sCube['int']['char']['<'] = sCube['char']['int']['<'] = 'char'
sCube['int']['char']['<>'] = sCube['char']['int']['<>'] = 'char'
sCube['int']['char']['=='] = sCube['char']['int']['=='] = 'char'
sCube['int']['char']['<='] = sCube['char']['int']['<='] = 'char'
sCube['int']['char']['>='] = sCube['char']['int']['>='] = 'char'
sCube['int']['char']['+'] = sCube['char']['int']['+'] = 'char'
sCube['int']['char']['-'] = sCube['char']['int']['-'] = 'char'
sCube['int']['char']['*'] = sCube['char']['int']['*'] = 'char'
sCube['int']['char']['/'] = sCube['char']['int']['/'] = 'char'
sCube['int']['char']['='] = 'int'
sCube['char']['int']['='] = 'char'

sCube['int']['bool']['and'] = sCube['bool']['int']['and'] = 'bool'
sCube['int']['bool']['or'] = sCube['bool']['int']['or'] = 'bool'
sCube['int']['bool']['>'] = sCube['bool']['int']['>'] = 'bool'
sCube['int']['bool']['<'] = sCube['bool']['int']['<'] = 'bool'
sCube['int']['bool']['<>'] = sCube['bool']['int']['<>'] = 'bool'
sCube['int']['bool']['=='] = sCube['bool']['int']['=='] = 'bool'
sCube['int']['bool']['<='] = sCube['bool']['int']['<='] = 'bool'
sCube['int']['bool']['>='] = sCube['bool']['int']['>='] = 'bool'
sCube['int']['bool']['+'] = sCube['bool']['int']['+'] = 'int'
sCube['int']['bool']['-'] = sCube['bool']['int']['-'] = 'int'
sCube['int']['bool']['*'] = sCube['bool']['int']['*'] = 'int'
sCube['int']['bool']['/'] = sCube['bool']['int']['/'] = 'int'
sCube['int']['bool']['='] = 'int'
sCube['bool']['int']['='] = 'bool'
sCube['float']['dynamic']['='] = 'float'

sCube['float']['char']['and'] = sCube['char']['float']['and'] = 'bool'
sCube['float']['char']['or'] = sCube['char']['float']['or'] = 'bool'
sCube['float']['char']['>'] = sCube['char']['float']['>'] = 'bool'
sCube['float']['char']['<'] = sCube['char']['float']['<'] = 'bool'
sCube['float']['char']['<>'] = sCube['char']['float']['<>'] = 'bool'
sCube['float']['char']['=='] = sCube['char']['float']['=='] = 'bool'
sCube['float']['char']['<='] = sCube['char']['float']['<='] = 'bool'
sCube['float']['char']['>='] = sCube['char']['float']['>='] = 'bool'
sCube['float']['char']['+'] = sCube['char']['float']['+'] = 'float'
sCube['float']['char']['-'] = sCube['char']['float']['-'] = 'float'
sCube['float']['char']['*'] = sCube['char']['float']['*'] = 'float'
sCube['float']['char']['/'] = sCube['char']['float']['/'] = 'float'
sCube['float']['char']['='] = 'float'
sCube['char']['float']['='] = 'char'
sCube['char']['dynamic']['='] = 'char'

sCube['float']['bool']['and'] = sCube['bool']['float']['and'] = 'bool'
sCube['float']['bool']['or'] = sCube['bool']['float']['or'] = 'bool'
sCube['float']['bool']['>'] = sCube['bool']['float']['>'] = 'bool'
sCube['float']['bool']['<'] = sCube['bool']['float']['<'] = 'bool'
sCube['float']['bool']['<>'] = sCube['bool']['float']['<>'] = 'bool'
sCube['float']['bool']['=='] = sCube['bool']['float']['=='] = 'bool'
sCube['float']['bool']['<='] = sCube['bool']['float']['<='] = 'bool'
sCube['float']['bool']['>='] = sCube['bool']['float']['>='] = 'bool'
sCube['float']['bool']['+'] = sCube['bool']['float']['+'] = 'float'
sCube['float']['bool']['-'] = sCube['bool']['float']['-'] = 'float'
sCube['float']['bool']['*'] = sCube['bool']['float']['*'] = 'float'
sCube['float']['bool']['/'] = sCube['bool']['float']['/'] = 'float'
sCube['float']['bool']['='] = 'float'
sCube['bool']['float']['='] = 'bool'
sCube['bool']['dynamic']['='] = 'bool'

sCube['char']['bool']['and'] = sCube['bool']['char']['and'] = 'bool'
sCube['char']['bool']['or'] = sCube['bool']['char']['or'] = 'bool'
sCube['char']['bool']['>'] = sCube['bool']['char']['>'] = 'bool'
sCube['char']['bool']['<'] = sCube['bool']['char']['<'] = 'bool'
sCube['char']['bool']['<>'] = sCube['bool']['char']['<>'] = 'bool'
sCube['char']['bool']['=='] = sCube['bool']['char']['=='] = 'bool'
sCube['char']['bool']['<='] = sCube['bool']['char']['<='] = 'bool'
sCube['char']['bool']['>='] = sCube['bool']['char']['>='] = 'bool'
sCube['char']['bool']['+'] = sCube['bool']['char']['+'] = 'char'
sCube['char']['bool']['-'] = sCube['bool']['char']['-'] = 'char'
sCube['char']['bool']['*'] = sCube['bool']['char']['*'] = 'char'
sCube['char']['bool']['/'] = sCube['bool']['char']['/'] = 'char'
sCube['char']['bool']['='] = 'char'
sCube['bool']['char']['='] = 'bool'
sCube['bool']['dynamic']['='] = 'bool'
