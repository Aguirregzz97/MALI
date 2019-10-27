from collections import defaultdict, deque

# Symbol table utils.

def new_var_dict(type, access=None):
  var_dict = {
    '#assigned' : True,
    '#type': type
  }
  if access: var_dict['#access'] = access
  return var_dict


def new_func_dict(type=None, access=None):
  func_dict = {
    '#param_count': 0,
    '#var_count': 0,
    '#vars': {}
  }
  if type: func_dict['#type'] = type
  if access: func_dict['#access'] = access
  return func_dict


def new_class_dict(parent='#global'):
  class_dict = {
    '#parent': parent,
    '#funcs': {
      '#attributes': new_func_dict()
    }
  }
  return class_dict


# Intermediate code generation utils

class available:
  nextT = 1
  avail = deque([])

  def next(self):

    if len(self.avail) == 0:
      nextTemp = 't' + str(self.nextT)
      self.nextT += 1
    else:
      nextTemp = 't' + str(self.avail.popleft())
    return nextTemp

  def free(self, temp):
    self.avail.append(temp[1:])



sCube = defaultdict(lambda : defaultdict(lambda : defaultdict(dict)))

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
