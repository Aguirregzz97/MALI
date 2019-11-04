# Constants used for MALI language.

from collections import defaultdict

# Memory addresses thresholds.
VAR_LOWER_LIMIT = 11000
VAR_UPPER_LIMIT = 15999
TEMP_LOWER_LIMIT = 16000
TEMP_UPPER_LIMIT = 19999
GLOBAL_ADJUSTMENT = 10000
INSTANCE_ADJUSTMENT = 5000
CONSTANT_LOWER_LIMIT = 20000
CONSTANT_UPPER_LIMIT = 24999


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

semantic_cube['int']['int']['and'] = 'bool'
semantic_cube['int']['int']['or'] = 'bool'
semantic_cube['int']['int']['>'] = 'bool'
semantic_cube['int']['int']['<'] = 'bool'
semantic_cube['int']['int']['<>'] = 'bool'
semantic_cube['int']['int']['=='] = 'bool'
semantic_cube['int']['int']['<='] = 'bool'
semantic_cube['int']['int']['>='] = 'bool'
semantic_cube['int']['int']['+'] = 'int'
semantic_cube['int']['int']['-'] = 'int'
semantic_cube['int']['int']['*'] = 'int'
semantic_cube['int']['int']['/'] = 'int'
semantic_cube['int']['int']['='] = 'int'
semantic_cube['int']['dynamic']['='] = 'int'

semantic_cube['float']['float']['and'] = 'bool'
semantic_cube['float']['float']['or'] = 'bool'
semantic_cube['float']['float']['>'] = 'bool'
semantic_cube['float']['float']['<'] = 'bool'
semantic_cube['float']['float']['<>'] = 'bool'
semantic_cube['float']['float']['=='] = 'bool'
semantic_cube['float']['float']['<='] = 'bool'
semantic_cube['float']['float']['>='] = 'bool'
semantic_cube['float']['float']['+'] = 'float'
semantic_cube['float']['float']['-'] = 'float'
semantic_cube['float']['float']['*'] = 'float'
semantic_cube['float']['float']['/'] = 'float'
semantic_cube['float']['float']['='] = 'float'
semantic_cube['float']['dynamic']['='] = 'float'

semantic_cube['char']['char']['and'] = 'bool'
semantic_cube['char']['char']['or'] = 'bool'
semantic_cube['char']['char']['>'] = 'bool'
semantic_cube['char']['char']['<'] = 'bool'
semantic_cube['char']['char']['<>'] = 'bool'
semantic_cube['char']['char']['=='] = 'bool'
semantic_cube['char']['char']['>='] = 'bool'
semantic_cube['char']['char']['<='] = 'bool'
semantic_cube['char']['char']['+'] = 'char'
semantic_cube['char']['char']['-'] = 'char'
semantic_cube['char']['char']['*'] = 'char'
semantic_cube['char']['char']['/'] = 'char'
semantic_cube['char']['char']['='] = 'char'
semantic_cube['char']['dynamic']['='] = 'char'

semantic_cube['bool']['bool']['and'] = 'bool'
semantic_cube['bool']['bool']['or'] = 'bool'
semantic_cube['bool']['bool']['>'] = 'bool'
semantic_cube['bool']['bool']['<'] = 'bool'
semantic_cube['bool']['bool']['<>'] = 'bool'
semantic_cube['bool']['bool']['=='] = 'bool'
semantic_cube['bool']['bool']['>='] = 'bool'
semantic_cube['bool']['bool']['<='] = 'bool'
semantic_cube['bool']['bool']['+'] = 'int'
semantic_cube['bool']['bool']['-'] = 'int'
semantic_cube['bool']['bool']['*'] = 'int'
semantic_cube['bool']['bool']['/'] = 'int'
semantic_cube['bool']['bool']['='] = 'bool'
semantic_cube['bool']['dynamic']['='] = 'bool'

semantic_cube['int']['float']['and'] = semantic_cube['float']['int']['and'] = 'bool'
semantic_cube['int']['float']['or'] = semantic_cube['float']['int']['or'] = 'bool'
semantic_cube['int']['float']['>'] = semantic_cube['float']['int']['>'] = 'bool'
semantic_cube['int']['float']['<'] = semantic_cube['float']['int']['<'] = 'bool'
semantic_cube['int']['float']['<>'] = semantic_cube['float']['int']['<>'] = 'bool'
semantic_cube['int']['float']['=='] = semantic_cube['float']['int']['=='] = 'bool'
semantic_cube['int']['float']['<='] = semantic_cube['float']['int']['<='] = 'bool'
semantic_cube['int']['float']['>='] = semantic_cube['float']['int']['>='] = 'bool'
semantic_cube['int']['float']['+'] = semantic_cube['float']['int']['+'] = 'float'
semantic_cube['int']['float']['-'] = semantic_cube['float']['int']['-'] = 'float'
semantic_cube['int']['float']['*'] = semantic_cube['float']['int']['*'] = 'float'
semantic_cube['int']['float']['/'] = semantic_cube['float']['int']['/'] = 'float'
semantic_cube['int']['float']['='] = 'int'
semantic_cube['float']['int']['='] = 'float'

semantic_cube['int']['char']['and'] = semantic_cube['char']['int']['and'] = 'char'
semantic_cube['int']['char']['or'] = semantic_cube['char']['int']['or'] = 'char'
semantic_cube['int']['char']['>'] = semantic_cube['char']['int']['>'] = 'char'
semantic_cube['int']['char']['<'] = semantic_cube['char']['int']['<'] = 'char'
semantic_cube['int']['char']['<>'] = semantic_cube['char']['int']['<>'] = 'char'
semantic_cube['int']['char']['=='] = semantic_cube['char']['int']['=='] = 'char'
semantic_cube['int']['char']['<='] = semantic_cube['char']['int']['<='] = 'char'
semantic_cube['int']['char']['>='] = semantic_cube['char']['int']['>='] = 'char'
semantic_cube['int']['char']['+'] = semantic_cube['char']['int']['+'] = 'char'
semantic_cube['int']['char']['-'] = semantic_cube['char']['int']['-'] = 'char'
semantic_cube['int']['char']['*'] = semantic_cube['char']['int']['*'] = 'char'
semantic_cube['int']['char']['/'] = semantic_cube['char']['int']['/'] = 'char'
semantic_cube['int']['char']['='] = 'int'
semantic_cube['char']['int']['='] = 'char'

semantic_cube['int']['bool']['and'] = semantic_cube['bool']['int']['and'] = 'bool'
semantic_cube['int']['bool']['or'] = semantic_cube['bool']['int']['or'] = 'bool'
semantic_cube['int']['bool']['>'] = semantic_cube['bool']['int']['>'] = 'bool'
semantic_cube['int']['bool']['<'] = semantic_cube['bool']['int']['<'] = 'bool'
semantic_cube['int']['bool']['<>'] = semantic_cube['bool']['int']['<>'] = 'bool'
semantic_cube['int']['bool']['=='] = semantic_cube['bool']['int']['=='] = 'bool'
semantic_cube['int']['bool']['<='] = semantic_cube['bool']['int']['<='] = 'bool'
semantic_cube['int']['bool']['>='] = semantic_cube['bool']['int']['>='] = 'bool'
semantic_cube['int']['bool']['+'] = semantic_cube['bool']['int']['+'] = 'int'
semantic_cube['int']['bool']['-'] = semantic_cube['bool']['int']['-'] = 'int'
semantic_cube['int']['bool']['*'] = semantic_cube['bool']['int']['*'] = 'int'
semantic_cube['int']['bool']['/'] = semantic_cube['bool']['int']['/'] = 'int'
semantic_cube['int']['bool']['='] = 'int'
semantic_cube['bool']['int']['='] = 'bool'
semantic_cube['float']['dynamic']['='] = 'float'

semantic_cube['float']['char']['and'] = semantic_cube['char']['float']['and'] = 'bool'
semantic_cube['float']['char']['or'] = semantic_cube['char']['float']['or'] = 'bool'
semantic_cube['float']['char']['>'] = semantic_cube['char']['float']['>'] = 'bool'
semantic_cube['float']['char']['<'] = semantic_cube['char']['float']['<'] = 'bool'
semantic_cube['float']['char']['<>'] = semantic_cube['char']['float']['<>'] = 'bool'
semantic_cube['float']['char']['=='] = semantic_cube['char']['float']['=='] = 'bool'
semantic_cube['float']['char']['<='] = semantic_cube['char']['float']['<='] = 'bool'
semantic_cube['float']['char']['>='] = semantic_cube['char']['float']['>='] = 'bool'
semantic_cube['float']['char']['+'] = semantic_cube['char']['float']['+'] = 'float'
semantic_cube['float']['char']['-'] = semantic_cube['char']['float']['-'] = 'float'
semantic_cube['float']['char']['*'] = semantic_cube['char']['float']['*'] = 'float'
semantic_cube['float']['char']['/'] = semantic_cube['char']['float']['/'] = 'float'
semantic_cube['float']['char']['='] = 'float'
semantic_cube['char']['float']['='] = 'char'
semantic_cube['char']['dynamic']['='] = 'char'

semantic_cube['float']['bool']['and'] = semantic_cube['bool']['float']['and'] = 'bool'
semantic_cube['float']['bool']['or'] = semantic_cube['bool']['float']['or'] = 'bool'
semantic_cube['float']['bool']['>'] = semantic_cube['bool']['float']['>'] = 'bool'
semantic_cube['float']['bool']['<'] = semantic_cube['bool']['float']['<'] = 'bool'
semantic_cube['float']['bool']['<>'] = semantic_cube['bool']['float']['<>'] = 'bool'
semantic_cube['float']['bool']['=='] = semantic_cube['bool']['float']['=='] = 'bool'
semantic_cube['float']['bool']['<='] = semantic_cube['bool']['float']['<='] = 'bool'
semantic_cube['float']['bool']['>='] = semantic_cube['bool']['float']['>='] = 'bool'
semantic_cube['float']['bool']['+'] = semantic_cube['bool']['float']['+'] = 'float'
semantic_cube['float']['bool']['-'] = semantic_cube['bool']['float']['-'] = 'float'
semantic_cube['float']['bool']['*'] = semantic_cube['bool']['float']['*'] = 'float'
semantic_cube['float']['bool']['/'] = semantic_cube['bool']['float']['/'] = 'float'
semantic_cube['float']['bool']['='] = 'float'
semantic_cube['bool']['float']['='] = 'bool'
semantic_cube['bool']['dynamic']['='] = 'bool'

semantic_cube['char']['bool']['and'] = semantic_cube['bool']['char']['and'] = 'bool'
semantic_cube['char']['bool']['or'] = semantic_cube['bool']['char']['or'] = 'bool'
semantic_cube['char']['bool']['>'] = semantic_cube['bool']['char']['>'] = 'bool'
semantic_cube['char']['bool']['<'] = semantic_cube['bool']['char']['<'] = 'bool'
semantic_cube['char']['bool']['<>'] = semantic_cube['bool']['char']['<>'] = 'bool'
semantic_cube['char']['bool']['=='] = semantic_cube['bool']['char']['=='] = 'bool'
semantic_cube['char']['bool']['<='] = semantic_cube['bool']['char']['<='] = 'bool'
semantic_cube['char']['bool']['>='] = semantic_cube['bool']['char']['>='] = 'bool'
semantic_cube['char']['bool']['+'] = semantic_cube['bool']['char']['+'] = 'char'
semantic_cube['char']['bool']['-'] = semantic_cube['bool']['char']['-'] = 'char'
semantic_cube['char']['bool']['*'] = semantic_cube['bool']['char']['*'] = 'char'
semantic_cube['char']['bool']['/'] = semantic_cube['bool']['char']['/'] = 'char'
semantic_cube['char']['bool']['='] = 'char'
semantic_cube['bool']['char']['='] = 'bool'
semantic_cube['bool']['dynamic']['='] = 'bool'
