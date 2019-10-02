import ply.lex as lex

reserved = {
  'class' : 'CLASS',
  'extends' : 'EXTENDS',
  'int' : 'INT',
  'float' : 'FLOAT',
  'char' : 'CHAR',
  'bool' : 'BOOL',
  'public' : 'PUBLIC',
  'private' : 'PRIVATE',
  'protected' : 'PROTECTED',
  'void' : 'VOID',
  'main' : 'MAIN',
  'func' : 'FUNCTION',
  'init' : 'INIT',
  'return' : 'RETURN',
  'and' : 'AND',
  'or' : 'OR',
  'not' : 'NOT',
  'true' : 'TRUE',
  'false' : 'FALSE',
  'read' : 'READ',
  'write' : 'WRITE',
  'if' : 'IF',
  'elif' : 'ELIF',
  'else' : 'ELSE',
  'while' : 'WHILE'
}

tokens = [
  'ID',
  'CTE_I',
  'CTE_F',
  'CTE_CH',
  'CTE_STR',
  'SC',
  'COLON',
  'COMMA',
  'DOT',
  'LEFT_P',
  'RIGHT_P',
  'LEFT_B',
  'RIGHT_B',
  'LEFT_SB',
  'RIGHT_SB',
  'PLUS',
  'MINUS',
  'TIMES',
  'DIV',
  'EQUAL',
  'ISEQUAL',
  'LESS_T',
  'MORE_T',
  'DIFFERENT',
  'LESS_ET',
  'MORE_ET'
] + list(reserved.values())

t_SC = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_LEFT_P = r'\('
t_RIGHT_P = r'\)'
t_LEFT_B = r'{'
t_RIGHT_B = r'}'
t_LEFT_SB = r'\['
t_RIGHT_SB = r'\]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/'
t_EQUAL = r'='
t_ISEQUAL = r'=='
t_LESS_T = r'<'
t_MORE_T = r'>'
t_DIFFERENT = r'<>'
t_LESS_ET = r'<='
t_MORE_ET = r'>='
t_CTE_STR = r'("[^"]*")'
t_CTE_CH = r'\'[A-Za-z]\''

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'ID')
  return t

def t_CTE_I(t):
  r'[-+]?[0-9]+'
  t.value = int(t.value)
  return t

def t_CTE_F(t):
  r'[-+]?[0-9]+(\.[0-9]+)?'
  t.value = float(t.value)
  return t

def t_newline(t):
  r'[\r\n]+'
  t.lexer.lineno += len(t.value)

def t_comment(t):
  r'\#.*\n'
  t.lexer.lineno += len(t.value)
  pass

t_ignore = ' \t'

def t_error(t):
  print("SCAN ERROR ", t)
  t.lexer.skip(1)

lexer = lex.lex()

'''------------------

lexer.input('main { }')

for tok in lexer:
  print(tok)

'''