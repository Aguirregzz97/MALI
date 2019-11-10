from memory import Memory

memory = Memory()
symbol_table = None
q = 0
end = False

def set_input(input):
    global data_segment, constant_segment, symbol_table
    for address, value in input['data_segment'].items():
        memory.set(address, value)
    for address, value in input['constant_segment'].items():
        memory.set(address, value)
    symbol_table = input['symbol_table']

def op_plus_unary(a, b, c):
    pass

def op_minus_unary(a, b, c):
    pass

def op_not(a, b, c):
    pass

def op_times(a, b, c):
    pass

def op_div(a, b, c):
    pass

def op_plus(a, b, c):
    memory.set(c, memory.get(a) + memory.get(b))

def op_minus(a, b, c):
    pass

def op_less_than(a, b, c):
    pass

def op_more_than(a, b, c):
    pass

def op_different(a, b, c):
    pass

def op_is_equal(a, b, c):
    pass

def op_less_equal(a, b, c):
    pass

def op_more_equal(a, b, c):
    pass

def op_or(a, b, c):
    pass

def op_and(a, b, c):
    pass

def op_equal(a, b, c):
    memory.set(c, memory.get(a))

def op_read(a, b, c):
    pass

def op_write(a, b, c):
    pass

def op_goto(a, b, c):
    global q
    q = c

def op_gotof(a, b, c):
    pass

def op_gosub(a, b, c):
    pass

def op_param(a, b, c):
    pass

def op_era(a, b, c):
    pass

def op_return(a, b, c):
    pass

def op_endproc(a, b, c):
    pass

def op_end(a, b, c):
    global end
    end = True

def op_switch_instance(a, b, c):
    pass

def op_exit_instances(a, b, c):
    pass

def op_get_return(a, b, c):
    pass

def op_fake_bottom(a, b, c):
    pass
