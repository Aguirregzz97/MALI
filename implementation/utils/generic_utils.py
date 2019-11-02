# Utils module for general use.

def top(l):
  if len(l) > 0:
    return l[-1]
  return None


class ValOrError:
  val = None
  error = None


def invert_dict(old_dict):
  return {v: k for k, v in old_dict.items()}