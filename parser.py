# Parser implementation for MALI language.

import ply.yacc as yacc
from scanner import tokens
import semantic as s
import sys

import pprint
pp = pprint.PrettyPrinter()

input_str = ''
error = False


# Parsing utilities.

def recover_parser():
  opened = 0
  tokName = None
  while True:
    tok = parser.token()
    if not tok: break
    tokName = tok.type
    if tokName == 'SC' and opened == 0:
      break
    elif tokName == 'LEFT_B':
      opened += 1
    elif tokName == 'RIGHT_B':
      opened -= 1
      if opened == 0: break
  parser.restart()
  return tokName

def add_to_tree(name, p):
  p[0] = tuple([name, *list(filter(None, p[1:]))])

def find_column(lexpos):
  line_start = input_str.rfind('\n', 0, lexpos) + 1
  return (lexpos - line_start) + 1


# Errors reporting.

def error_prefix(line, lexpos):
  print(f'Error at {line}:{find_column(lexpos)} - ', end='')
  global error
  error = True

def handle_error(line, lexpos, mssg):
  #raise SyntaxError
  error_prefix(line, lexpos)
  print(mssg)
  recover_parser()


# Syntax rules.

def p_program(p):
  '''program : classes vars modules main
             | classes modules main
             | modules main
             | vars modules main
             | classes main
             | vars main
             | main'''
  add_to_tree('program', p)
  #pp.pprint(p[0])
  #pp.pprint(s.classes)
  if handle_error:
      sys.exit(-1)

def p_classes(p):
  '''classes : class classes
             | class'''
  add_to_tree('classes', p)

def p_class(p):
  '''class : CLASS ID r_seenClass classblock r_finishClass
           | CLASS ID r_seenClass EXTENDS ID r_classParent classblock \
             r_finishClass'''
  add_to_tree('class', p)

def p_classblock(p):
  '''classblock : LEFT_B attributes init methods RIGHT_B
                | LEFT_B init methods RIGHT_B
                | LEFT_B attributes init RIGHT_B
                | LEFT_B init RIGHT_B'''
  add_to_tree('classblock', p)

def p_attributes(p):
  '''attributes : ATTR r_seenAttr LEFT_B attr_dec RIGHT_B'''
  add_to_tree('attributes', p)

def p_attr_dec(p):
  '''attr_dec : access var attr_dec
              | access var'''
  add_to_tree('attr_dec', p)

def p_init(p):
  '''init : INIT r_seenInit LEFT_P param RIGHT_P init_factor'''
  add_to_tree('init', p)

def p_init_factor(p):
  '''init_factor : proc_block
                 | COLON ID r_callParent LEFT_P expression RIGHT_P \
                   proc_block '''
  add_to_tree('init_factor', p)

def p_methods(p):
  '''methods : access proc r_isMethod methods
             | access proc r_isMethod'''
  add_to_tree('methods', p)

def p_access(p):
  '''access : PUBLIC r_seenAccess
            | PRIVATE r_seenAccess
            | PROTECTED r_seenAccess'''
  add_to_tree('access', p)

def p_vars(p):
  '''vars : VAR LEFT_B vars_dec RIGHT_B'''
  add_to_tree('vars', p)

def p_vars_dec(p):
  '''vars_dec : var vars_dec
              | var'''
  add_to_tree('vars_dec', p)

def p_var(p):
  '''var : type var_aux SC'''
  add_to_tree('var', p)

def p_var_aux(p):
  '''var_aux : ID r_varName COMMA var_aux
             | ID r_varName
             | ID r_varName arr_index COMMA var_aux
             | ID r_varName arr_index'''
  add_to_tree('var_aux', p)

def p_type(p):
  '''type : INT r_seenType
          | FLOAT r_seenType
          | CHAR r_seenType
          | BOOL r_seenType
          | ID r_seenType '''
  add_to_tree('type', p)

def p_1(p):
  '''modules : FUNCTION proc modules
             | FUNCTION proc'''
  add_to_tree('modules', p)

def p_proc(p):
  '''proc : type ID r_funcName LEFT_P param RIGHT_P proc_block
          | VOID r_seenType ID r_funcName LEFT_P param RIGHT_P proc_block'''
  add_to_tree('proc', p)

def p_proc_block(p):
  '''proc_block : LEFT_B vars statements RIGHT_B
                | LEFT_B vars RIGHT_B
                | block'''
  add_to_tree('proc_block', p)

def p_param(p):
  '''param : r_seenParam params r_finishParam
           | empty'''
  add_to_tree('param', p)

def p_params(p):
  '''params : type ID r_varName COMMA params
            | type ID r_varName
            | type ID r_varName arr_index COMMA params
            | type ID r_varName arr_index'''
  add_to_tree('params', p)

def p_statements(p):
  '''statements : statement SC statements
                | statement SC'''
  add_to_tree('statements', p)

def p_statement(p):
  '''statement : assign
               | call
               | return
               | write
               | if
               | while'''
  add_to_tree('statement', p)

def p_assign(p):
  '''assign : ID arr_index EQUAL expression
            | ID arr_index EQUAL READ
            | ID EQUAL expression
            | ID EQUAL READ'''
  add_to_tree('assign', p)

def p_call(p):
  '''call : path LEFT_P expression RIGHT_P
          | path LEFT_P RIGHT_P
          | path_aux '''
  add_to_tree('call', p)

def p_path(p):
  '''path : ID DOT path
          | ID'''
  add_to_tree('path', p)

def p_path_aux(p):
  '''path_aux : ID DOT path'''
  add_to_tree('path_aux', p)

def p_return(p):
  '''return : RETURN expression'''
  add_to_tree('return', p)

def p_write(p):
  '''write : WRITE words'''
  add_to_tree('write', p)

def p_words(p):
  '''words : CTE_STR COMMA words
           | CTE_STR
           | expression COMMA words
           | expression'''
  add_to_tree('words', p)

def p_if(p):
  '''if : IF condition'''
  add_to_tree('if', p)

def p_condition(p):
  '''condition : LEFT_P expression RIGHT_P block ELIF condition
               | LEFT_P expression RIGHT_P block ELSE block
               | LEFT_P expression RIGHT_P block'''
  add_to_tree('condition', p)

def p_while(p):
  '''while : WHILE LEFT_P expression RIGHT_P block'''
  add_to_tree('while', p)

def p_expression(p):
  '''expression : exp AND exp
                | exp'''
  add_to_tree('expression', p)

def p_exp(p):
  '''exp : xp OR xp
         | xp'''
  add_to_tree('exp', p)

def p_xp(p):
  '''xp : x
        | x MORE_T x
        | x LESS_T x
        | x DIFFERENT x
        | x ISEQUAL x
        | x LESS_ET x
        | x MORE_ET x'''
  add_to_tree('xp', p)

def p_x(p):
  '''x : term PLUS x
       | term MINUS x
       | term'''
  add_to_tree('x', p)

def p_term(p):
  '''term : factor TIMES term
          | factor DIV term
          | factor'''
  add_to_tree('term', p)

def p_factor(p):
  '''factor : not LEFT_P expression RIGHT_P
            | not sign cte'''
  add_to_tree('factor', p)

def p_not(p):
  '''not : NOT
         | empty'''
  add_to_tree('not', p)

def p_sign(p):
  '''sign : PLUS
         | MINUS
         | empty'''
  add_to_tree('sign', p)

def p_cte(p):
  '''cte : ID
         | CTE_I
         | CTE_F
         | CTE_CH
         | TRUE
         | FALSE
         | arraccess
         | call'''
  add_to_tree('cte', p)

def p_arraccess(p):
  '''arraccess : ID arr_index'''
  add_to_tree('arraccess', p)

def p_arr_index(p):
  '''arr_index : LEFT_SB expression RIGHT_SB
               | LEFT_SB expression RIGHT_SB LEFT_SB expression RIGHT_SB'''
  add_to_tree('arr_index', p)

def p_block(p):
  '''block : LEFT_B statements RIGHT_B
           | LEFT_B RIGHT_B'''
  add_to_tree('block', p)

def p_main(p):
  '''main : MAIN r_seenMain proc_block'''
  add_to_tree('main', p)

# Rule used to create an cfg epsilon-like value.
def p_empty(p):
  '''empty :'''
  add_to_tree('empty', p)

# Syntax error detection rules.

def p_e_program_missing_main(p):
  '''program : classes vars modules
             | classes modules
             | modules
             | vars modules
             | classes
             | vars'''
  handle_error(input_str.count('\n'), input_str.rfind('\n'), 'Missing main block.')

def p_e_program_main_not_end(p):
  '''program : classes vars modules main error
             | classes modules main error
             | modules main error
             | vars modules main error
             | classes main error
             | vars main error
             | main error'''
  pos = len(p)-1
  handle_error(p.lineno(pos), p.lexpos(pos), 'The code should end with the main block.')

def p_e_program_disorder(p):
  '''program : vars classes error
             | modules classes error
             | vars modules classes error
             | modules vars error'''
  handle_error(0, 0, 'Bad program structure, should be: classes -> global vars -> modules -> main')


# Syntax error printing.

def p_error(p):
  error_prefix(p.lineno, p.lexpos)
  print(f'Unexpected token {p.value}.')


# Semantic rules.

def p_r_seenClass(p):
  'r_seenClass : '
  e = s.seenClass(class_name=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_classParent(p):
  'r_classParent : '
  e = s.classParent(class_parent=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_finishClass(p):
  'r_finishClass : '
  s.finishClass()

def p_r_seenAttr(p):
  'r_seenAttr : '
  s.seenFunc(new_function='#attributes')

def p_r_seenAccess(p):
  'r_seenAccess : '
  s.seenAccess(new_access=p[-1])

def p_r_seenType(p):
  'r_seenType : '
  e = s.seenType(new_type=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_varName(p):
  'r_varName : '
  e = s.varName(var_name=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenInit(p):
  'r_seenInit : '
  e = s.seenFunc(new_function='init')
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenParam(p):
  'r_seenParam : '
  s.setParam(True)

def p_r_finishParam(p):
  'r_finishParam : '
  s.setParam(False)

def p_r_callParent(p):
  'r_callParent : '
  e = s.callParent(parent=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_funcName(p):
  'r_funcName : '
  e = s.seenFunc(new_function=p[-1], recordType=True)
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_isMethod(p):
  'r_isMethod : '
  s.isMethod()

def p_r_seenMain(p):
  'r_seenMain : '
  e = s.seenFunc(new_function='#main')
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)


# Generate parser.
parser = yacc.yacc(start='program')
parser.defaulted_states = {}

# Run parser.

def set_input_str(s):
  global input_str
  input_str = s

def parseString(s):
  global input_str
  set_input_str(s)
  try:
    parser.parse(s, tracking=True)
  except:
    pass
