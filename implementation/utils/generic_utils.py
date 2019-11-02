def top(l):
  if len(l) > 0:
    return l[-1]
  return None

class ValOrError:
  val = None
  error = None

class Available:
  def __init__(self, begin, limit):
    #self._prefix = prefix
    self.__begin = begin
    self.__next = begin
    self.__limit = limit

  def next(self):
    #next = self._prefix + str(self._next)
    self.__next += 1
    if self.__next > self.__limit:
      return None
    return self.__next

  def reset(self):
    self.__next = self.__begin