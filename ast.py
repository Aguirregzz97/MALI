import pydot
from mali import program_name

i = 0

def draw_tree(dot_data):
    (graph,) = pydot.graph_from_dot_data(dot_data)
    graph.write_png(f'{program_name}_model_tree.png')


def get_val(p):
    if isinstance(p, tuple):
        return f'"{p[0]}"'
    else:
        return f'"{p}"'

# WIP
def tuples_to_dot_data(p):
    if isinstance(p, tuple) and len(p) > 1:
        global i
        parent = p[0] # f'{p[0]} [{i}]'
        i = i + 1
        return f'"{parent}"->' + f';"{parent}"->'.join([str(get_val(item)) for item in p[1:]]) + ';' + ''.join([tuples_to_dot_data(item) for item in p[1:]])
    return ''


def gen_ast(p):
    dot_data = 'digraph {' + tuples_to_dot_data(p) + '}'
    print(dot_data)
    draw_tree(dot_data)
