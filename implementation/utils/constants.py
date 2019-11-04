# Constants used for MALI language.

from collections import defaultdict
from enum import Enum, IntEnum, auto

# Memory addresses thresholds.
VAR_LOWER_LIMIT = 11000
VAR_UPPER_LIMIT = 15999
TEMP_LOWER_LIMIT = 16000
TEMP_UPPER_LIMIT = 19999
GLOBAL_ADJUSTMENT = 10000
INSTANCE_ADJUSTMENT = 5000
CONSTANT_LOWER_LIMIT = 20000
CONSTANT_UPPER_LIMIT = 24999

# Language data types.
class Types(Enum):
  INT = 'int'
  FLOAT = 'float'
  CHAR = 'char'
  BOOL = 'bool'
  CTE_STRING = 'cte_string'
  CLASS = 'class'
  VOID = 'void'
  READ = 'read'


var_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL, Types.CLASS)
temp_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL)
const_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL,
               Types.CTE_STRING)
func_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL, Types.VOID)


class Access(Enum):
  PUBLIC = 'public'
  PRIVATE = 'private'
  PROTECTED = 'protected'

str_access = {
  'public' : Access.PUBLIC,
  'private' : Access.PRIVATE,
  'protected' : Access.PROTECTED
}


class Operations(IntEnum):
  PLUS_UNARY = 1
  MINUS_UNARY = 2
  NOT = 3
  TIMES = 4
  DIV = 5
  PLUS = 6
  MINUS = 7
  LESS_THAN = 8
  MORE_THAN = 9
  DIFFERENT = 10
  IS_EQUAL = 11
  LESS_EQUAL = 12
  MORE_EQUAL = 13
  OR = 14
  AND = 15
  EQUAL = 16
  READ = 17
  WRITE = 18
  GOTO = 19
  GOTOF = 20
  GOSUB = 21
  PARAM = 22
  ERA = 23
  RETURN = 24
  ENDPROC = 25
  END = 26
  SWITCH_INSTANCE = 27
  EXIT_INSTANCES = 28
  GET_RETURN = 29
  FAKE_BOTTOM = 30

str_operations = {
  'unary+': Operations.PLUS_UNARY,
  'unary-': Operations.MINUS_UNARY,
  'unarynot': Operations.NOT,
  '*': Operations.TIMES,
  '/': Operations.DIV,
  '+': Operations.PLUS,
  '-': Operations.MINUS,
  '<': Operations.LESS_THAN,
  '>': Operations.MORE_THAN,
  '<>': Operations.DIFFERENT,
  '==': Operations.IS_EQUAL,
  '<=': Operations.LESS_EQUAL,
  '>=': Operations.MORE_EQUAL,
  'or': Operations.OR,
  'and': Operations.AND,
  '=': Operations.EQUAL,
  '(': Operations.FAKE_BOTTOM
}


semantic_cube = defaultdict(lambda : defaultdict(lambda : defaultdict(
    lambda : defaultdict(None))))

semantic_cube[Types.INT][Types.INT][Operations.AND] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.OR] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.INT][Operations.PLUS] = Types.INT
semantic_cube[Types.INT][Types.INT][Operations.MINUS] = Types.INT
semantic_cube[Types.INT][Types.INT][Operations.TIMES] = Types.INT
semantic_cube[Types.INT][Types.INT][Operations.DIV] = Types.INT
semantic_cube[Types.INT][Types.INT][Operations.EQUAL] = Types.INT
semantic_cube[Types.INT][Types.READ][Operations.EQUAL] = Types.INT

semantic_cube[Types.FLOAT][Types.FLOAT][Operations.AND] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.OR] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.PLUS] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.MINUS] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.TIMES] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.DIV] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT][Operations.EQUAL] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.READ][Operations.EQUAL] = Types.FLOAT

semantic_cube[Types.CHAR][Types.CHAR][Operations.AND] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.OR] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR][Operations.PLUS] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR][Operations.MINUS] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR][Operations.TIMES] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR][Operations.DIV] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR][Operations.EQUAL] = Types.CHAR
semantic_cube[Types.CHAR][Types.READ][Operations.EQUAL] = Types.CHAR

semantic_cube[Types.BOOL][Types.BOOL][Operations.AND] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.OR] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL][Operations.PLUS] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL][Operations.MINUS] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL][Operations.TIMES] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL][Operations.DIV] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL][Operations.EQUAL] = Types.BOOL
semantic_cube[Types.BOOL][Types.READ][Operations.EQUAL] = Types.BOOL

semantic_cube[Types.INT][Types.FLOAT][Operations.AND] = semantic_cube[Types.FLOAT][Types.INT][Operations.AND] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.OR] = semantic_cube[Types.FLOAT][Types.INT][Operations.OR] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.LESS_THAN] = semantic_cube[Types.FLOAT][Types.INT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.MORE_THAN] = semantic_cube[Types.FLOAT][Types.INT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.DIFFERENT] = semantic_cube[Types.FLOAT][Types.INT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.IS_EQUAL] = semantic_cube[Types.FLOAT][Types.INT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.LESS_EQUAL] = semantic_cube[Types.FLOAT][Types.INT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.MORE_EQUAL] = semantic_cube[Types.FLOAT][Types.INT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT][Operations.PLUS] = semantic_cube[Types.FLOAT][Types.INT][Operations.PLUS] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT][Operations.MINUS] = semantic_cube[Types.FLOAT][Types.INT][Operations.MINUS] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT][Operations.TIMES] = semantic_cube[Types.FLOAT][Types.INT][Operations.TIMES] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT][Operations.DIV] = semantic_cube[Types.FLOAT][Types.INT][Operations.DIV] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT][Operations.EQUAL] = Types.INT
semantic_cube[Types.FLOAT][Types.INT][Operations.EQUAL] = Types.FLOAT

semantic_cube[Types.INT][Types.CHAR][Operations.AND] = semantic_cube[Types.CHAR][Types.INT][Operations.AND] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.OR] = semantic_cube[Types.CHAR][Types.INT][Operations.OR] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.LESS_THAN] = semantic_cube[Types.CHAR][Types.INT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.MORE_THAN] = semantic_cube[Types.CHAR][Types.INT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.DIFFERENT] = semantic_cube[Types.CHAR][Types.INT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.IS_EQUAL] = semantic_cube[Types.CHAR][Types.INT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.LESS_EQUAL] = semantic_cube[Types.CHAR][Types.INT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.MORE_EQUAL] = semantic_cube[Types.CHAR][Types.INT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.CHAR][Operations.PLUS] = semantic_cube[Types.CHAR][Types.INT][Operations.PLUS] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR][Operations.MINUS] = semantic_cube[Types.CHAR][Types.INT][Operations.MINUS] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR][Operations.TIMES] = semantic_cube[Types.CHAR][Types.INT][Operations.TIMES] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR][Operations.DIV] = semantic_cube[Types.CHAR][Types.INT][Operations.DIV] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR][Operations.EQUAL] = Types.INT
semantic_cube[Types.CHAR][Types.INT][Operations.EQUAL] = Types.CHAR

semantic_cube[Types.INT][Types.BOOL][Operations.AND] = semantic_cube[Types.BOOL][Types.INT][Operations.AND] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.OR] = semantic_cube[Types.BOOL][Types.INT][Operations.OR] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.LESS_THAN] = semantic_cube[Types.BOOL][Types.INT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.MORE_THAN] = semantic_cube[Types.BOOL][Types.INT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.DIFFERENT] = semantic_cube[Types.BOOL][Types.INT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.IS_EQUAL] = semantic_cube[Types.BOOL][Types.INT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.LESS_EQUAL] = semantic_cube[Types.BOOL][Types.INT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.MORE_EQUAL] = semantic_cube[Types.BOOL][Types.INT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL][Operations.PLUS] = semantic_cube[Types.BOOL][Types.INT][Operations.PLUS] = Types.INT
semantic_cube[Types.INT][Types.BOOL][Operations.MINUS] = semantic_cube[Types.BOOL][Types.INT][Operations.MINUS] = Types.INT
semantic_cube[Types.INT][Types.BOOL][Operations.TIMES] = semantic_cube[Types.BOOL][Types.INT][Operations.TIMES] = Types.INT
semantic_cube[Types.INT][Types.BOOL][Operations.DIV] = semantic_cube[Types.BOOL][Types.INT][Operations.DIV] = Types.INT
semantic_cube[Types.INT][Types.BOOL][Operations.EQUAL] = Types.INT
semantic_cube[Types.BOOL][Types.INT][Operations.EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.READ][Operations.EQUAL] = Types.FLOAT

semantic_cube[Types.FLOAT][Types.CHAR][Operations.AND] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.AND] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.OR] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.OR] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.LESS_THAN] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.MORE_THAN] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.DIFFERENT] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.IS_EQUAL] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.LESS_EQUAL] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.MORE_EQUAL] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR][Operations.PLUS] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.PLUS] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR][Operations.MINUS] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.MINUS] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR][Operations.TIMES] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.TIMES] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR][Operations.DIV] = semantic_cube[Types.CHAR][Types.FLOAT][Operations.DIV] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR][Operations.EQUAL] = Types.FLOAT
semantic_cube[Types.CHAR][Types.FLOAT][Operations.EQUAL] = Types.CHAR
semantic_cube[Types.CHAR][Types.READ][Operations.EQUAL] = Types.CHAR

semantic_cube[Types.FLOAT][Types.BOOL][Operations.AND] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.AND] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.OR] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.OR] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.LESS_THAN] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.MORE_THAN] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.DIFFERENT] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.IS_EQUAL] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.LESS_EQUAL] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.MORE_EQUAL] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL][Operations.PLUS] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.PLUS] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL][Operations.MINUS] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.MINUS] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL][Operations.TIMES] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.TIMES] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL][Operations.DIV] = semantic_cube[Types.BOOL][Types.FLOAT][Operations.DIV] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL][Operations.EQUAL] = Types.FLOAT
semantic_cube[Types.BOOL][Types.FLOAT][Operations.EQUAL] = Types.BOOL
semantic_cube[Types.BOOL][Types.READ][Operations.EQUAL] = Types.BOOL

semantic_cube[Types.CHAR][Types.BOOL][Operations.AND] = semantic_cube[Types.BOOL][Types.CHAR][Operations.AND] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.OR] = semantic_cube[Types.BOOL][Types.CHAR][Operations.OR] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.LESS_THAN] = semantic_cube[Types.BOOL][Types.CHAR][Operations.LESS_THAN] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.MORE_THAN] = semantic_cube[Types.BOOL][Types.CHAR][Operations.MORE_THAN] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.DIFFERENT] = semantic_cube[Types.BOOL][Types.CHAR][Operations.DIFFERENT] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.IS_EQUAL] = semantic_cube[Types.BOOL][Types.CHAR][Operations.IS_EQUAL] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.LESS_EQUAL] = semantic_cube[Types.BOOL][Types.CHAR][Operations.LESS_EQUAL] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.MORE_EQUAL] = semantic_cube[Types.BOOL][Types.CHAR][Operations.MORE_EQUAL] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL][Operations.PLUS] = semantic_cube[Types.BOOL][Types.CHAR][Operations.PLUS] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL][Operations.MINUS] = semantic_cube[Types.BOOL][Types.CHAR][Operations.MINUS] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL][Operations.TIMES] = semantic_cube[Types.BOOL][Types.CHAR][Operations.TIMES] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL][Operations.DIV] = semantic_cube[Types.BOOL][Types.CHAR][Operations.DIV] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL][Operations.EQUAL] = Types.CHAR
semantic_cube[Types.BOOL][Types.CHAR][Operations.EQUAL] = Types.BOOL
semantic_cube[Types.BOOL][Types.READ][Operations.EQUAL] = Types.BOOL
