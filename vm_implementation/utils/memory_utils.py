# Utilities for MALI language's memory.

from vm_implementation.utils.constants import *  # pylint: disable=unused-wildcard-import
import sys


class Error:
  '''Prints error message and stops execution.'''

  def __init__(self, message: str):
    print("\nError:", message)
    sys.exit()


def top(l):
  '''Gets the top element on a stack without crashing if stack is empty.'''
  if len(l) > 0:
    return l[-1]
  return None


def cast_value(cast_type: Types, value):
  '''Casts raw value to given type.'''
  value_type = type(value)
  if value is None:
    return None
  if cast_type == Types.INT:
    if value_type == str:
      value = float(value)
    try:
      return int(value)
    except:
      Error('Cannot cast int.')
  elif cast_type == Types.FLOAT:
    try:
      return float(value)
    except:
      Error('Cannot cast float.')
  elif cast_type == Types.CHAR:
    try:
      if value <= 0 or value >= sys.maxunicode:
        Error('Char overflow')
      return int(value)
    except:
      Error('Cannot cast char.')
  elif cast_type == Types.BOOL:
    try:
      return int(bool(value))
    except:
      Error('Cannot cast bool.')
  else:
    Error(f'Unrecognized type {cast_type}.')
