# Parsing utilities.


def recover_parser(parser):
  '''Recovers parser on error to keep finding errors.'''

  opened = 0
  tokName = None
  while True:
    tok = parser.token()
    if not tok:
      break
    tokName = tok.type
    if tokName == 'SC' and opened == 0:
      break
    elif tokName == 'LEFT_B':
      opened += 1
    elif tokName == 'RIGHT_B':
      opened -= 1
      if opened == 0:
        break
  parser.restart()
  return tokName


def find_column(lexpos, input_str: str):
  '''Finds the column where an error ocurred.

  This is used to display error messages.
  '''

  line_start = input_str.rfind('\n', 0, lexpos) + 1
  return (lexpos - line_start) + 1


def error_prefix(line, lexpos, input_str):
  '''Prints the line and column where an error ocurred.'''

  print(f'Error at {line}:{find_column(lexpos, input_str)} - ', end='')
  global error
  error = True
