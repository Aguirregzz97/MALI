def top(l):
  if len(l) > 0:
    return l[-1]
  return None

class val_or_error():
  val = None
  error = None