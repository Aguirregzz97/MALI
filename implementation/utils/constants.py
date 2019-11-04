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
  INT = auto()
  FLOAT = auto()
  CHAR = auto()
  BOOL = auto()
  CTE_STRING = auto()
  CLASS = auto()
  VOID = auto()
  READ = auto()


var_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL, Types.CLASS)
temp_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL)
const_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL,
               Types.CTE_STRING)
func_types = (Types.INT, Types.FLOAT, Types.CHAR, Types.BOOL, Types.VOID)


operations = {
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
  'end': 26,
  'switch_instance': 27,
  'exit_instances': 28,
  'get_return': 29
}


semantic_cube = defaultdict(lambda : defaultdict(lambda : defaultdict(
    lambda : defaultdict(None))))

semantic_cube[Types.INT][Types.INT]['and'] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['or'] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['>'] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['<'] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['<>'] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['=='] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['<='] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['>='] = Types.BOOL
semantic_cube[Types.INT][Types.INT]['+'] = Types.INT
semantic_cube[Types.INT][Types.INT]['-'] = Types.INT
semantic_cube[Types.INT][Types.INT]['*'] = Types.INT
semantic_cube[Types.INT][Types.INT]['/'] = Types.INT
semantic_cube[Types.INT][Types.INT]['='] = Types.INT
semantic_cube[Types.INT][Types.READ]['='] = Types.INT

semantic_cube[Types.FLOAT][Types.FLOAT]['and'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['or'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['>'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['<'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['<>'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['=='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['<='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['>='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.FLOAT]['+'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT]['-'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT]['*'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT]['/'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.FLOAT]['='] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.READ]['='] = Types.FLOAT

semantic_cube[Types.CHAR][Types.CHAR]['and'] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['or'] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['>'] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['<'] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['<>'] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['=='] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['>='] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['<='] = Types.BOOL
semantic_cube[Types.CHAR][Types.CHAR]['+'] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR]['-'] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR]['*'] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR]['/'] = Types.CHAR
semantic_cube[Types.CHAR][Types.CHAR]['='] = Types.CHAR
semantic_cube[Types.CHAR][Types.READ]['='] = Types.CHAR

semantic_cube[Types.BOOL][Types.BOOL]['and'] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['or'] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['>'] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['<'] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['<>'] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['=='] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['>='] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['<='] = Types.BOOL
semantic_cube[Types.BOOL][Types.BOOL]['+'] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL]['-'] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL]['*'] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL]['/'] = Types.INT
semantic_cube[Types.BOOL][Types.BOOL]['='] = Types.BOOL
semantic_cube[Types.BOOL][Types.READ]['='] = Types.BOOL

semantic_cube[Types.INT][Types.FLOAT]['and'] = semantic_cube[Types.FLOAT][Types.INT]['and'] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['or'] = semantic_cube[Types.FLOAT][Types.INT]['or'] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['>'] = semantic_cube[Types.FLOAT][Types.INT]['>'] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['<'] = semantic_cube[Types.FLOAT][Types.INT]['<'] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['<>'] = semantic_cube[Types.FLOAT][Types.INT]['<>'] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['=='] = semantic_cube[Types.FLOAT][Types.INT]['=='] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['<='] = semantic_cube[Types.FLOAT][Types.INT]['<='] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['>='] = semantic_cube[Types.FLOAT][Types.INT]['>='] = Types.BOOL
semantic_cube[Types.INT][Types.FLOAT]['+'] = semantic_cube[Types.FLOAT][Types.INT]['+'] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT]['-'] = semantic_cube[Types.FLOAT][Types.INT]['-'] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT]['*'] = semantic_cube[Types.FLOAT][Types.INT]['*'] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT]['/'] = semantic_cube[Types.FLOAT][Types.INT]['/'] = Types.FLOAT
semantic_cube[Types.INT][Types.FLOAT]['='] = Types.INT
semantic_cube[Types.FLOAT][Types.INT]['='] = Types.FLOAT

semantic_cube[Types.INT][Types.CHAR]['and'] = semantic_cube[Types.CHAR][Types.INT]['and'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['or'] = semantic_cube[Types.CHAR][Types.INT]['or'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['>'] = semantic_cube[Types.CHAR][Types.INT]['>'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['<'] = semantic_cube[Types.CHAR][Types.INT]['<'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['<>'] = semantic_cube[Types.CHAR][Types.INT]['<>'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['=='] = semantic_cube[Types.CHAR][Types.INT]['=='] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['<='] = semantic_cube[Types.CHAR][Types.INT]['<='] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['>='] = semantic_cube[Types.CHAR][Types.INT]['>='] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['+'] = semantic_cube[Types.CHAR][Types.INT]['+'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['-'] = semantic_cube[Types.CHAR][Types.INT]['-'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['*'] = semantic_cube[Types.CHAR][Types.INT]['*'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['/'] = semantic_cube[Types.CHAR][Types.INT]['/'] = Types.CHAR
semantic_cube[Types.INT][Types.CHAR]['='] = Types.INT
semantic_cube[Types.CHAR][Types.INT]['='] = Types.CHAR

semantic_cube[Types.INT][Types.BOOL]['and'] = semantic_cube[Types.BOOL][Types.INT]['and'] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['or'] = semantic_cube[Types.BOOL][Types.INT]['or'] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['>'] = semantic_cube[Types.BOOL][Types.INT]['>'] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['<'] = semantic_cube[Types.BOOL][Types.INT]['<'] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['<>'] = semantic_cube[Types.BOOL][Types.INT]['<>'] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['=='] = semantic_cube[Types.BOOL][Types.INT]['=='] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['<='] = semantic_cube[Types.BOOL][Types.INT]['<='] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['>='] = semantic_cube[Types.BOOL][Types.INT]['>='] = Types.BOOL
semantic_cube[Types.INT][Types.BOOL]['+'] = semantic_cube[Types.BOOL][Types.INT]['+'] = Types.INT
semantic_cube[Types.INT][Types.BOOL]['-'] = semantic_cube[Types.BOOL][Types.INT]['-'] = Types.INT
semantic_cube[Types.INT][Types.BOOL]['*'] = semantic_cube[Types.BOOL][Types.INT]['*'] = Types.INT
semantic_cube[Types.INT][Types.BOOL]['/'] = semantic_cube[Types.BOOL][Types.INT]['/'] = Types.INT
semantic_cube[Types.INT][Types.BOOL]['='] = Types.INT
semantic_cube[Types.BOOL][Types.INT]['='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.READ]['='] = Types.FLOAT

semantic_cube[Types.FLOAT][Types.CHAR]['and'] = semantic_cube[Types.CHAR][Types.FLOAT]['and'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['or'] = semantic_cube[Types.CHAR][Types.FLOAT]['or'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['>'] = semantic_cube[Types.CHAR][Types.FLOAT]['>'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['<'] = semantic_cube[Types.CHAR][Types.FLOAT]['<'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['<>'] = semantic_cube[Types.CHAR][Types.FLOAT]['<>'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['=='] = semantic_cube[Types.CHAR][Types.FLOAT]['=='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['<='] = semantic_cube[Types.CHAR][Types.FLOAT]['<='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['>='] = semantic_cube[Types.CHAR][Types.FLOAT]['>='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.CHAR]['+'] = semantic_cube[Types.CHAR][Types.FLOAT]['+'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR]['-'] = semantic_cube[Types.CHAR][Types.FLOAT]['-'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR]['*'] = semantic_cube[Types.CHAR][Types.FLOAT]['*'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR]['/'] = semantic_cube[Types.CHAR][Types.FLOAT]['/'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.CHAR]['='] = Types.FLOAT
semantic_cube[Types.CHAR][Types.FLOAT]['='] = Types.CHAR
semantic_cube[Types.CHAR][Types.READ]['='] = Types.CHAR

semantic_cube[Types.FLOAT][Types.BOOL]['and'] = semantic_cube[Types.BOOL][Types.FLOAT]['and'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['or'] = semantic_cube[Types.BOOL][Types.FLOAT]['or'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['>'] = semantic_cube[Types.BOOL][Types.FLOAT]['>'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['<'] = semantic_cube[Types.BOOL][Types.FLOAT]['<'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['<>'] = semantic_cube[Types.BOOL][Types.FLOAT]['<>'] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['=='] = semantic_cube[Types.BOOL][Types.FLOAT]['=='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['<='] = semantic_cube[Types.BOOL][Types.FLOAT]['<='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['>='] = semantic_cube[Types.BOOL][Types.FLOAT]['>='] = Types.BOOL
semantic_cube[Types.FLOAT][Types.BOOL]['+'] = semantic_cube[Types.BOOL][Types.FLOAT]['+'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL]['-'] = semantic_cube[Types.BOOL][Types.FLOAT]['-'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL]['*'] = semantic_cube[Types.BOOL][Types.FLOAT]['*'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL]['/'] = semantic_cube[Types.BOOL][Types.FLOAT]['/'] = Types.FLOAT
semantic_cube[Types.FLOAT][Types.BOOL]['='] = Types.FLOAT
semantic_cube[Types.BOOL][Types.FLOAT]['='] = Types.BOOL
semantic_cube[Types.BOOL][Types.READ]['='] = Types.BOOL

semantic_cube[Types.CHAR][Types.BOOL]['and'] = semantic_cube[Types.BOOL][Types.CHAR]['and'] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['or'] = semantic_cube[Types.BOOL][Types.CHAR]['or'] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['>'] = semantic_cube[Types.BOOL][Types.CHAR]['>'] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['<'] = semantic_cube[Types.BOOL][Types.CHAR]['<'] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['<>'] = semantic_cube[Types.BOOL][Types.CHAR]['<>'] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['=='] = semantic_cube[Types.BOOL][Types.CHAR]['=='] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['<='] = semantic_cube[Types.BOOL][Types.CHAR]['<='] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['>='] = semantic_cube[Types.BOOL][Types.CHAR]['>='] = Types.BOOL
semantic_cube[Types.CHAR][Types.BOOL]['+'] = semantic_cube[Types.BOOL][Types.CHAR]['+'] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL]['-'] = semantic_cube[Types.BOOL][Types.CHAR]['-'] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL]['*'] = semantic_cube[Types.BOOL][Types.CHAR]['*'] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL]['/'] = semantic_cube[Types.BOOL][Types.CHAR]['/'] = Types.CHAR
semantic_cube[Types.CHAR][Types.BOOL]['='] = Types.CHAR
semantic_cube[Types.BOOL][Types.CHAR]['='] = Types.BOOL
semantic_cube[Types.BOOL][Types.READ]['='] = Types.BOOL
