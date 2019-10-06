# Parser implementation for MALI language.

import ply.yacc as yacc
from scanner import tokens
from semanticTables import *

import pprint
pp = pprint.PrettyPrinter(depth=6)

# Syntax rules.

def p_program(p):
  '''program : classes vars modules main
             | classes modules main
             | modules main
             | vars modules main
             | classes main
             | vars main
             | main'''

def p_classes(p):
  '''classes : class classes
             | class'''

def p_class(p):
  '''class : CLASS ID r_seenClass classblock r_finishClass
           | CLASS ID r_seenClass EXTENDS ID r_classParent classblock \
             r_finishClass'''

def p_classblock(p):
  '''classblock : LEFT_B attributes init methods RIGHT_B
                | LEFT_B init methods RIGHT_B
                | LEFT_B attributes init RIGHT_B
                | LEFT_B init RIGHT_B'''

def p_attributes(p):
  '''attributes : ATTR r_seenAttr LEFT_B attr_dec RIGHT_B'''

def p_attr_dec(p):
  '''attr_dec : access var attr_dec
              | access var'''

def p_init(p):
  '''init : INIT ID LEFT_P param RIGHT_P init_factor'''

def p_init_factor(p):
  '''init_factor : proc_block
                 | COLON ID LEFT_P expression RIGHT_P proc_block '''

def p_methods(p):
  '''methods : access proc methods
             | access proc'''

def p_access(p):
  '''access : PUBLIC r_seenAccess
            | PRIVATE r_seenAccess
            | PROTECTED r_seenAccess'''

def p_vars(p):
  '''vars : VAR LEFT_B vars_dec RIGHT_B'''

def p_vars_dec(p):
  '''vars_dec : var vars_dec
              | var'''

def p_var(p):
  '''var : type var_aux SC'''

def p_var_aux(p):
  '''var_aux : ID r_varName COMMA var_aux
             | ID r_varName
             | ID r_varName arr_index COMMA var_aux
             | ID r_varName arr_index'''

def p_type(p):
  '''type : INT r_seenType 
          | FLOAT r_seenType 
          | CHAR r_seenType 
          | BOOL r_seenType 
          | ID r_seenType '''

def p_modules(p):
  '''modules : FUNCTION proc modules
             | FUNCTION proc'''

def p_proc(p):
  '''proc : type ID LEFT_P param RIGHT_P proc_block
          | VOID ID LEFT_P param RIGHT_P proc_block'''

def p_proc_block(p):
  '''proc_block : LEFT_B vars statements RIGHT_B
                | LEFT_B vars RIGHT_B
                | block'''

def p_param(p):
  '''param : params
           | empty'''

def p_params(p):
  '''params : type ID COMMA params 
            | type ID 
            | type ID arr_index COMMA params 
            | type ID arr_index''' 

def p_statements(p):
  '''statements : statement SC statements
                | statement SC'''

def p_statement(p):
  '''statement : assign
               | call
               | return
               | write
               | if
               | while'''

def p_assign(p):
  '''assign : ID arr_index EQUAL expression 
            | ID arr_index EQUAL READ 
            | ID EQUAL expression 
            | ID EQUAL READ'''

def p_call(p):
  '''call : path LEFT_P expression RIGHT_P
          | path LEFT_P RIGHT_P
          | path_aux '''

def p_path(p):
  '''path : ID DOT path
          | ID'''

def p_path_aux(p):
  '''path_aux : ID DOT path'''

def p_return(p):
  '''return : RETURN expression'''

def p_write(p):
  '''write : WRITE words'''

def p_words(p):
  '''words : CTE_STR COMMA words
           | CTE_STR
           | expression COMMA words
           | expression'''

def p_if(p):
  '''if : IF condition'''

def p_condition(p):
  '''condition : LEFT_P expression RIGHT_P block ELIF condition 
               | LEFT_P expression RIGHT_P block ELSE block 
               | LEFT_P expression RIGHT_P block''' 

def p_while(p):
  '''while : WHILE LEFT_P expression RIGHT_P block'''

def p_expression(p):
  '''expression : exp AND exp
                | exp'''

def p_exp(p):
  '''exp : xp OR xp
         | xp'''

def p_xp(p):
  '''xp : x
        | x MORE_T x
        | x LESS_T x
        | x DIFFERENT x
        | x ISEQUAL x
        | x LESS_ET x
        | x MORE_ET x'''

def p_x(p):
  '''x : term PLUS x
       | term MINUS x
       | term'''

def p_term(p):
  '''term : factor TIMES term
          | factor DIV term
          | factor'''

def p_factor(p):
  '''factor : not LEFT_P expression RIGHT_P
            | not sign cte'''

def p_not(p):
  '''not : NOT
         | empty'''

def p_sign(p):
  '''sign : PLUS
         | MINUS
         | empty'''

def p_cte(p):
  '''cte : ID
         | CTE_I
         | CTE_F
         | CTE_CH
         | TRUE
         | FALSE
         | arraccess
         | call'''

def p_arraccess(p):
  '''arraccess : ID arr_index'''

def p_arr_index(p):
  '''arr_index : LEFT_SB expression RIGHT_SB
               | LEFT_SB expression RIGHT_SB LEFT_SB expression RIGHT_SB'''

def p_block(p):
  '''block : LEFT_B statements RIGHT_B
           | LEFT_B RIGHT_B'''

def p_main(p):
  '''main : MAIN proc_block'''

def p_empty(p):
  '''empty :'''

def p_error(p):
  print("Error! ", p)

# Semantic rules

def p_r_seenClass(p):
  'r_seenClass : '

  class_name = p[-1]
  if class_name in classes:
    p_error(f"Repeated class name: {class_name}")
  else:
    global current_class
    current_class = class_name
    classes[class_name] = new_class_dict()


def p_r_classParent(p):
  'r_classParent : '
  
  class_parent = p[-1]
  if class_parent not in classes:
    p_error(f"Undeclared class parent: {class_parent}")
  else:
    classes[current_class]['parent'] = class_parent


def p_r_finishClass(p):
  'r_finishClass : '

  global current_class
  current_class = 'global'


def p_r_seenAttr(p):
  'r_seenAttr : '

  global current_function
  current_function = 'global'
  classes[current_class][current_function] = new_func_dict(name='attributes')


def p_r_seenAccess(p):
  'r_seenAccess : '

  global current_access
  current_access = p[-1]


def p_r_seenType(p):
  'r_seenType : '

  global current_type
  current_type = p[-1]


def p_r_varName(p):
  'r_varName : '

  var_name = p[-1]
  if var_name in classes[current_class][current_function]:
    p_error(f"Redeclared variable: {var_name}")
  else:
    if current_class != 'global':
      classes[current_class][current_function][var_name] = (
          new_var_dict(type=current_type, access=current_access))
    else:
      classes[current_class][current_function][var_name] = (
          new_var_dict(type=current_type))

# Build parser.
parser = yacc.yacc(start='program')
