import ply.lex as lex

tokens = (
  'ID',
  'CLASS',
  'EXTENDS',
  'INT',
  'FLOAT',
  'CHAR',
  'BOOL',
  'PUBLIC',
  'PRIVATE',
  'PROTECTED',
  'VOID',
  'MAIN',
  'FUNCTION',
  'INIT',
  'RETURN',
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
  'MORE_ET',
  'AND',
  'OR',
  'NOT',
  'TRUE',
  'FALSE',
  'READ',
  'WRITE',
  'IF',
  'ELIF',
  'ELSE',
  'WHILE',
)

t_CLASS = r'class'
t_EXTENDS = r'extends'
t_INT = r'int'
t_FLOAT = r'float'
t_CHAR = r'char'
t_BOOL = r'bool'
t_PUBLIC = r'public'
t_PRIVATE = r'private'
t_PROTECTED = r't_protected'
t_VOID = r'void'
t_MAIN = r'main'
t_FUNCTION = r'func'
t_INIT = r'init'
t_RETURN = r'return'
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
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_TRUE = r'true'
t_FALSE = r'false'
t_READ = r'read'
t_WRITE = r'write'
t_IF = r'if'
t_ELIF = r'elif'
t_ELSE = r'else'
t_WHILE = r'while'
t_ID = r'[a-z][a-zA-Z]*'
t_CTE_STR = r'("[^"]*")'
t_CTE_CH = r'\'[A-Za-z]\''

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

t_ignore = r' \t'

def t_error(t):
  print("SCAN ERROR ", t)
  t.lexer.skip(1)

lexer = lex.lex()

lexer.input('main { }')

for tok in lexer:
  print(tok)
