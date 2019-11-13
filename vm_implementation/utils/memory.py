from vm_implementation.utils.constants import *  # pylint: disable=unused-wildcard-import

symbol_table = None


class Values:
  def __init__(self, begin):
    self.__int_slots = {}
    self.__float_slots = {}
    self.__char_slots = {}
    self.__bool_slots = {}
    self.__instance_slots = {}

    self.__int_begin = begin
    self.__int_limit = self.__int_begin + BLOCK_SIZE - 1
    self.__float_begin = self.__int_limit + 1
    self.__float_limit = self.__float_begin + BLOCK_SIZE - 1
    self.__char_begin = self.__float_limit + 1
    self.__char_limit = self.__char_begin + BLOCK_SIZE - 1
    self.__bool_begin = self.__char_limit + 1
    self.__bool_limit = self.__bool_begin + BLOCK_SIZE - 1
    self.__instance_pointer_begin = self.__bool_limit + 1
    self.__instance_pointer_limit = self.__instance_pointer_begin + BLOCK_SIZE - 1

  def set(self, address, value, assign=False):

    if self.__int_begin <= address <= self.__int_limit:
      self.__int_slots[address] = value
    elif self.__float_begin <= address <= self.__float_limit:
      self.__float_slots[address] = value
    elif self.__char_begin <= address <= self.__char_limit:
      self.__char_slots[address] = value
    elif self.__bool_begin <= address <= self.__bool_limit:
      self.__bool_slots[address] = value
    elif self.__instance_pointer_begin <= address <= self.__instance_pointer_limit:
      self.__instance_slots[address] = InstanceMemory(value)
    else:
      raise Exception(f"Values.Set {address}: valor fuera del rango")

  def get(self, address):
    if self.__int_begin <= address <= self.__int_limit:
      return self.__int_slots.get(address, None)
    elif self.__float_begin <= address <= self.__float_limit:
      return self.__float_slots.get(address, None)
    elif self.__char_begin <= address <= self.__char_limit:
      return self.__char_slots.get(address, None)
    elif self.__bool_begin <= address <= self.__bool_limit:
      return self.__bool_slots.get(address, None)
    elif self.__instance_pointer_begin <= address <= self.__instance_pointer_limit:
      return self.__instance_slots.get(address, None)
    else:
      raise Exception(f"Values.Get {address}: valor fuera del rango")

  def print_values(self, prefix):
    print(prefix, 'int', self.__int_slots)
    print(prefix, 'float', self.__float_slots)
    print(prefix, 'char', self.__char_slots)
    print(prefix, 'bool', self.__bool_slots)
    for address, instance in self.__instance_slots.items():
      print(prefix, 'class', address)
      instance.print_instance(prefix + '\t')
    print()


class ProcedureMemory:
  def __init__(self):
    self.__vars = Values(VAR_LOWER_LIMIT)
    self.__temps = Values(TEMP_LOWER_LIMIT)

  def set(self, address, value):
    if VAR_LOWER_LIMIT <= address <= VAR_UPPER_LIMIT:
      self.__vars.set(address, value)
    elif TEMP_LOWER_LIMIT <= address <= TEMP_UPPER_LIMIT:
      self.__temps.set(address, value)
    else:
      raise Exception(f"ProcedureMemory.Set {address}: valor fuera del rango")

  def get(self, address):
    if VAR_LOWER_LIMIT <= address <= VAR_UPPER_LIMIT:
      return self.__vars.get(address)
    elif TEMP_LOWER_LIMIT <= address <= TEMP_UPPER_LIMIT:
      return self.__temps.get(address)
    else:
      raise Exception(f"ProcedureMemory.Get {address}: valor fuera del rango")

  def print_procedure(self, prefix):
    print(prefix, 'vars')
    self.__vars.print_values(prefix + '\t')
    print(prefix, 'temps')
    self.__temps.print_values(prefix + '\t')


class InstanceMemory:
  def __init__(self, class_name):
    self.__attributes = {}
    self.__attributes_stack = []
    self.__procedure_stack = []
    self.__next_procedure = None
    self.__next_attributes = None

    self.set_attributes(class_name)
    if class_name != '#global':
      attributes = symbol_table[class_name]['#funcs']['#attributes']['#vars'].values(
      )
      for attribute in attributes:
        self.set(attribute['#address'], attribute['#type'])

    curr_class = symbol_table[class_name]['#parent']
    while curr_class:
      self.set_attributes(curr_class)
      curr_attributes = symbol_table[curr_class]['#funcs']['#attributes']['#vars'].values(
      )
      for attribute in curr_attributes:
        self.set(attribute['#address'], attribute['#type'])
      curr_class = symbol_table[curr_class]['#parent']

    self.__attributes_stack = [list(self.__attributes.keys())[0]]

  def set(self, address, value, assigning_param=False):
    if ATTRIBUTE_LOWER_LIMIT <= address <= ATTRIBUTE_UPPER_LIMIT:
      self.__attributes[self.__attributes_stack[-1]].set(address, value)
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      if assigning_param:
        self.__next_procedure.set(address, value)
      else:
        self.__procedure_stack[-1].set(address, value)
    else:
      raise Exception(f"InstanceMemory.Set {address}: valor fuera del rango")

  def get(self, address):
    if ATTRIBUTE_LOWER_LIMIT <= address <= ATTRIBUTE_UPPER_LIMIT:
      for attribute in list(self.__attributes.values())[len(self.__attributes_stack)-1:]:
        value = attribute.get(address)
        if value is not None:
          return value
      return
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      return self.__procedure_stack[-1].get(address)
    else:
      raise Exception(f"InstanceMemory.Get {address}: valor fuera del rango")

  def set_attributes(self, class_name):
    self.__attributes[class_name] = Values(ATTRIBUTE_LOWER_LIMIT)
    self.__attributes_stack.append(class_name)

  def push_attributes(self, class_name):
    if top(self.__attributes_stack) != class_name:
      self.__attributes_stack.append(class_name)

  def pop_attributes(self):
    if len(self.__attributes_stack) > 1:
      self.__attributes_stack.pop()

  def prepare_new_procedure(self, class_name, func_name):
    self.__next_attributes = class_name
    self.__next_procedure = ProcedureMemory()
    var = symbol_table[class_name]['#funcs'][func_name]['#vars'].values()
    for v in var:
      self.__next_procedure.set(v['#address'], v['#type'])

  def push_new_procedure(self):
    if top(self.__attributes_stack) != self.__next_attributes:
      self.__attributes_stack.append(self.__next_attributes)
    self.__procedure_stack.append(self.__next_procedure)

  def pop_procedure(self):
    self.__procedure_stack.pop()
    if len(self.__attributes_stack) > 1:
      self.__attributes_stack.pop()

  def print_instance(self, prefix):
    print(prefix, 'attributes > current:', top(self.__attributes_stack), '\n')
    for class_name, attribute in self.__attributes.items():
      print(prefix + '\t', class_name)
      attribute.print_values(prefix + '\t')
    print(prefix, 'procedures')
    prefix += '\t'
    for procedure in self.__procedure_stack:
      procedure.print_procedure(prefix)
    if self.__next_procedure:
      print(prefix, 'next procedure')
      self.__next_procedure.print_procedure(prefix)


class Memory:
  def __init__(self, st):
    global symbol_table
    symbol_table = st
    self.__data_segment = Values(DATA_LOWER_LIMIT)
    self.__constant_segment = Values(CTE_LOWER_LIMIT)
    self.__instance_stack = [InstanceMemory('#global')]
    self.__return = None

    self.__setting_param = False
    self.__depth = 0
    self.prepare_new_procedure('#global', '#main')
    self.push_new_procedure()
    self.__depth = 0

  def set(self, address, value, assigning_param=False):
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      self.__data_segment.set(address, value)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      self.__constant_segment.set(address, value)
    else:
      if self.__setting_param and not assigning_param:
        self.__instance_stack[self.__depth-1].set(address, value)
      else:
        self.__instance_stack[-1].set(address, value, self.__setting_param)

  def get(self, address, assigning_param=False):
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      value = self.__data_segment.get(address)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      value = self.__constant_segment.get(address)
    else:
      if assigning_param:
        value = self.__instance_stack[self.__depth-1].get(address)
      else:
        value = self.__instance_stack[-1].get(address)
    if value is None:
      raise Exception(f'Value for {address} not found')
    return value

  def push_instance(self, address, class_name):
    self.__depth -= 1
    self.__instance_stack.append(self.get(address))
    self.__instance_stack[-1].push_attributes(class_name)

  def pop_instance(self):
    if self.__depth < 0:
      self.__depth += 1
    self.__instance_stack[-1].pop_attributes()
    self.__instance_stack.pop()

  def prepare_new_procedure(self, class_name, func_name):
    self.__setting_param = True
    self.__instance_stack[-1].prepare_new_procedure(class_name, func_name)

  def push_new_procedure(self):
    self.__setting_param = False
    self.__depth = 0
    self.__instance_stack[-1].push_new_procedure()

  def pop_procedure(self):
    self.__instance_stack[-1].pop_procedure()

  def set_return(self, value):
    self.__return = value

  def get_return(self):
    return_val = self.__return
    self.__return = None
    return return_val

  def print_memory(self):
    print('Data segment')
    self.__data_segment.print_values('\t')
    print('Constant segment')
    self.__constant_segment.print_values('\t')
    print('Instance stack')
    for instance in self.__instance_stack:
      instance.print_instance('\t')


def top(l):
  if len(l) > 0:
    return l[-1]
  return None
