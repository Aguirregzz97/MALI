# Utils module for general use.

def top(l):
  if len(l) > 0:
    return l[-1]
  return None

class ValOrError:
  val = None
  error = None