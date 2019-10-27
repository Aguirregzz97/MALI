# Parser implementation for MALI language.

import ply.yacc as yacc
from implementation.scanner import tokens
import implementation.semantic_and_quadruples as sq
from implementation.utils.parser_utils import *
import sys

import pprint, json
pp = pprint.PrettyPrinter()

input_str = ''
error = False

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
  #print(json.dumps(sq.classes, indent=4))
  pp.pprint(sq.classes)

  qCount = 0
  for quadruple in sq.quadruples:
    print(qCount, quadruple)
    qCount += 1
  #print(sq.jumps, sq.operands)

  if error:
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
  '''attributes : ATTR r_seenAttr LEFT_B attr_dec RIGHT_B r_endVars'''
  add_to_tree('attributes', p)

def p_attr_dec(p):
  '''attr_dec : access var attr_dec
              | access var'''
  add_to_tree('attr_dec', p)

def p_init(p):
  '''init : INIT r_seenInit LEFT_P param RIGHT_P init_factor r_finishFunc'''
  add_to_tree('init', p)

def p_init_factor(p):
  '''init_factor : r_startFunc proc_block
                 | COLON ID r_callParent param_pass \
                   r_startFunc proc_block '''
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
  '''vars : VAR LEFT_B vars_dec RIGHT_B r_endVars'''
  add_to_tree('vars', p)

def p_vars_dec(p):
  '''vars_dec : var vars_dec
              | var'''
  add_to_tree('vars_dec', p)

def p_var(p):
  '''var : complex_type var_aux SC'''
  add_to_tree('var', p)

def p_var_aux(p):
  '''var_aux : ID r_varName COMMA var_aux
             | ID r_varName
             | ID r_varName arr_dim COMMA var_aux
             | ID r_varName arr_dim'''
  add_to_tree('var_aux', p)

def p_arr_dim(p):
  '''arr_dim : LEFT_SB CTE_I RIGHT_SB
             | LEFT_SB CTE_I RIGHT_SB LEFT_SB CTE_I RIGHT_SB'''

def p_type(p):
  '''type : INT r_seenType
          | FLOAT r_seenType
          | CHAR r_seenType
          | BOOL r_seenType'''
  add_to_tree('type', p)

def p_complex_type(p):
  '''complex_type : type
                  | ID r_seenType'''

def p_modules(p):
  '''modules : FUNCTION proc modules
             | FUNCTION proc'''
  add_to_tree('modules', p)

def p_proc(p):
  '''proc : type ID r_funcName LEFT_P param RIGHT_P r_startFunc proc_block r_finishFunc
          | VOID r_seenType ID r_funcName LEFT_P param RIGHT_P r_startFunc \
            proc_block r_finishFunc'''
  add_to_tree('proc', p)

def p_proc_block(p):
  '''proc_block : LEFT_B vars statements RIGHT_B
                | LEFT_B vars RIGHT_B
                | block'''
  add_to_tree('proc_block', p)

def p_param(p):
  '''param : r_seenParam params r_finishParam
           | r_seenParam r_finishParam'''
  add_to_tree('param', p)

def p_params(p):
  '''params : complex_type ID r_varName COMMA params
            | complex_type ID r_varName
            | complex_type ID r_varName arr_index COMMA params
            | complex_type ID r_varName arr_index'''
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
            | ID arr_index EQUAL READ r_doRead
            | ID EQUAL expression
            | ID EQUAL READ r_doRead'''
  sq.doAssign(p[1])
  add_to_tree('assign', p)

def p_call(p):
  '''call : path param_pass
          | path_aux '''
  add_to_tree('call', p)

def p_param_pass(p):
  '''param_pass : LEFT_P r_startParams RIGHT_P r_doneParamPass
                | LEFT_P r_startParams param_pass_aux RIGHT_P r_doneParamPass'''
  add_to_tree('param_pass', p)

def p_param_pass_aux(p):
  '''param_pass_aux : expression r_passParam COMMA r_nextParamPass param_pass_aux
                    | expression r_passParam '''
  add_to_tree('param_pass_aux', p)

def p_path(p):
  '''path : ID DOT path
          | ID r_seenCall'''
  add_to_tree('path', p)

def p_path_aux(p):
  '''path_aux : ID DOT path'''
  add_to_tree('path_aux', p)

def p_return(p):
  '''return : RETURN expression r_seenReturn'''
  add_to_tree('return', p)

def p_write(p):
  '''write : WRITE words'''
  add_to_tree('write', p)

def p_words(p):
  '''words : CTE_STR r_doWriteStr COMMA words
           | CTE_STR r_doWriteStr
           | expression r_doWrite COMMA words
           | expression r_doWrite'''
  add_to_tree('words', p)

def p_if(p):
  '''if : IF condition'''
  add_to_tree('if', p)

def p_condition(p):
  '''condition : LEFT_P expression RIGHT_P r_seenCond block ELIF \
                 r_seenElse condition r_seenEndIf
               | LEFT_P expression RIGHT_P r_seenCond block ELSE \
                 r_seenElse block r_seenEndIf
               | LEFT_P expression RIGHT_P r_seenCond block r_seenEndIf'''
  add_to_tree('condition', p)

def p_while(p):
  '''while : WHILE r_seenWhile LEFT_P expression RIGHT_P r_seenCond block \
             r_seenEndWhile'''
  add_to_tree('while', p)

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
  '''main : MAIN r_seenMain proc_block r_finishMain'''
  add_to_tree('main', p)

def p_expression(p):
  '''expression : exp r_seenExp AND r_seenOperator expression
                | exp r_seenExp'''
  add_to_tree('expression', p)

def p_exp(p):
  '''exp : xp r_seenXp OR r_seenOperator exp
         | xp r_seenXp'''
  add_to_tree('exp', p)

def p_xp(p):
  '''xp : x r_seenX MORE_T r_seenOperator xp
        | x r_seenX LESS_T r_seenOperator xp
        | x r_seenX DIFFERENT r_seenOperator xp
        | x r_seenX ISEQUAL r_seenOperator xp
        | x r_seenX LESS_ET r_seenOperator xp
        | x r_seenX MORE_ET r_seenOperator xp
        | x r_seenX'''
  add_to_tree('xp', p)

def p_x(p):
  '''x : term r_seenTerm PLUS r_seenOperator x
       | term r_seenTerm MINUS r_seenOperator x
       | term r_seenTerm'''
  add_to_tree('x', p)

def p_term(p):
  '''term : factor r_seenFactor TIMES r_seenOperator term
          | factor r_seenFactor DIV r_seenOperator term
          | factor r_seenFactor'''
  add_to_tree('term', p)

def p_factor(p):
  '''factor : not LEFT_P r_seenOperator expression RIGHT_P r_popFakeBottom
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
  '''cte : ID r_seenOperand
         | CTE_I r_seenOperand
         | CTE_F r_seenOperand
         | CTE_CH r_seenOperand
         | arraccess
         | call'''
  add_to_tree('cte', p)

# Rule used to create an cfg epsilon-like value.
def p_empty(p):
  '''empty :'''
  add_to_tree('empty', p)

# Semantic rules.

def p_r_seenClass(p):
  'r_seenClass : '
  e = sq.seenClass(class_name=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_classParent(p):
  'r_classParent : '
  e = sq.classParent(class_parent=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_finishClass(p):
  'r_finishClass : '
  sq.finishClass()

def p_r_seenAttr(p):
  'r_seenAttr : '
  sq.seenFunc(new_function='#attributes')

def p_r_seenAccess(p):
  'r_seenAccess : '
  sq.seenAccess(new_access=p[-1])

def p_r_seenType(p):
  'r_seenType : '
  e = sq.seenType(new_type=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_varName(p):
  'r_varName : '
  e = sq.varName(var_name=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenInit(p):
  'r_seenInit : '
  sq.setVoid()
  e = sq.seenFunc(new_function='init')
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenParam(p):
  'r_seenParam : '
  sq.setParam(True)

def p_r_finishParam(p):
  'r_finishParam : '
  sq.setParam(False)

def p_r_callParent(p):
  'r_callParent : '
  e = sq.callParent(parent=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_funcName(p):
  'r_funcName : '
  e = sq.seenFunc(new_function=p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_isMethod(p):
  'r_isMethod : '
  sq.isMethod()

def p_r_seenMain(p):
  'r_seenMain : '
  sq.setVoid()
  sq.seenMain()
  e = sq.seenFunc(new_function='#main')
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenOperand(p):
  'r_seenOperand : '
  e = sq.seenOperand(p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenOperator(p):
  'r_seenOperator : '
  sq.seenOperator(p[-1])

def p_r_seenFactor(p):
  'r_seenFactor : '
  sq.seenSubRule(['*', '/'])

def p_r_seenTerm(p):
  'r_seenTerm : '
  sq.seenSubRule(['+', '-'])

def p_r_seenX(p):
  'r_seenX : '
  sq.seenSubRule(['>', '<', '<>', '==', '<=', '>='])

def p_r_seenXp(p):
  'r_seenXp : '
  sq.seenSubRule(['or'])

def p_r_seenExp(p):
  'r_seenExp : '
  sq.seenSubRule(['and'])

def p_r_popFakeBottom(p):
  'r_popFakeBottom : '
  sq.popFakeBottom()

def p_r_doWriteStr(p):
  'r_doWriteStr : '
  sq.doWrite(p[-1])

def p_r_doWrite(p):
  'r_doWrite : '
  sq.doWrite(None)

def p_r_doRead(p):
  'r_doRead : '
  sq.doRead()

def p_r_seenCond(p):
  'r_seenCond : '
  e = sq.seenCondition()
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_seenElse(p):
  'r_seenElse : '
  sq.seenElse()

def p_r_seenEndIf(p):
  'r_seenEndIf : '
  sq.seenEndIf()

def p_r_seenWhile(p):
  'r_seenWhile : '
  sq.seenWhile()

def p_r_seenEndWhile(p):
  'r_seenEndWhile : '
  sq.seenEndWhile()

def p_r_endVars(p):
  'r_endVars : '
  sq.endVars()

def p_r_startFunc(p):
  'r_startFunc : '
  sq.startFunc()

def p_r_finishFunc(p):
  'r_finishFunc : '
  sq.finishFunc()

def p_r_finishMain(p):
  'r_finishMain : '
  sq.finishFunc(is_main=True)

def p_r_seenReturn(p):
  'r_seenReturn : '
  sq.seenReturn()

def p_r_seenCall(p):
  'r_seenCall : '
  e = sq.seenCall(p[-1])
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_startParams(p):
  'r_startParams : '
  sq.startParams()

def p_r_passParam(p):
  'r_passParam : '
  e = sq.passParam()
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

def p_r_nextPassParam(p):
  'r_nextParamPass : '
  sq.r_nextParamPass()

def p_r_doneParamPass(p):
  'r_doneParamPass : '
  e = sq.doneParamPass()
  if e: handle_error(p.lineno(-1), p.lexpos(-1), e)

# Syntax error detection rules.

def p_e_program_missing_main(p):
  '''program : classes vars modules
             | classes modules
             | modules
             | vars modules
             | classes
             | vars'''
  handle_error(input_str.count('\n'), input_str.rfind('\n'),
               'Missing main block.')

def p_e_program_main_not_end(p):
  '''program : classes vars modules main error
             | classes modules main error
             | modules main error
             | vars modules main error
             | classes main error
             | vars main error
             | main error'''
  pos = len(p)-1
  handle_error(p.lineno(pos), p.lexpos(pos),
               'The code should end with the main block.')

def p_e_program_disorder(p):
  '''program : vars classes error
             | modules classes error
             | vars modules classes error
             | modules vars error'''
  handle_error(0, 0, 'Bad program structure, should be: classes -> ' +
               'global vars -> modules -> main')

# Syntax error printing.

def handle_error(line, lexpos, mssg):
  error_prefix(line, lexpos, input_str)
  print(mssg)
  recover_parser(parser)

def p_error(p):
  error_prefix(p.lineno, p.lexpos, input_str)
  print(f'Unexpected token {p.value}.')


# Generate parser.
parser = yacc.yacc(start='program')
parser.defaulted_states = {}

# Run parser.

def parseString(s):
  global input_str
  input_str = s
  parser.parse(s, tracking=True)
