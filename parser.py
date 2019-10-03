# Parser implementation for MALI language.

import ply.yacc as yacc
from scanner import tokens

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
  '''class : CLASS ID classblock 
           | CLASS ID EXTENDS ID classblock'''

def p_classblock(p):
  '''classblock : LEFT_B attributes init methods RIGHT_B
                | LEFT_B init methods RIGHT_B 
                | LEFT_B attributes init RIGHT_B
                | LEFT_B init RIGHT_B'''

def p_attributes(p):
  '''attributes : access var attributes
                | access var'''

def p_init(p):
  '''init : INIT ID LEFT_P param RIGHT_P init_factor'''

def p_init_factor(p):
  '''init_factor : proc_block
                 | COLON ID LEFT_P param RIGHT_P proc_block '''

def p_methods(p):
  '''methods : access proc methods 
             | access proc'''

def p_access(p):
  '''access : PUBLIC 
            | PRIVATE 
            | PROTECTED'''

def p_vars(p):
  '''vars : var vars
          | var'''

def p_var(p):
  '''var : type var_aux SC'''

def p_var_aux(p):
  '''var_aux : ID COMMA var_aux
             | ID
             | ID arr_index COMMA var_aux
             | ID arr_index'''

def p_type(p):
  '''type : INT 
          | FLOAT 
          | CHAR 
          | BOOL
          | ID'''

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
          | path LEFT_P RIGHT_P'''

def p_path(p):
  '''path : ID DOT path 
          | ID'''

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
  '''expression : exp 
                | exp AND exp 
                | exp OR exp  
                | exp MORE_T exp 
                | exp LESS_T exp 
                | exp DIFFERENT exp 
                | exp ISEQUAL exp 
                | exp LESS_ET exp 
                | exp MORE_ET exp'''

def p_exp(p):
  '''exp : term PLUS exp 
         | term MINUS exp 
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
         | MINUS'''

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
  '''main : MAIN block'''

def p_empty(p):
  '''empty :'''

def p_error(p):
  print("Syntax error in input! ", p)

# Build parser.
parser = yacc.yacc(start='program')

result = parser.parse('main { }')
print(result)