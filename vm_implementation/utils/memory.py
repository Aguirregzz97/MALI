# Memomry structure used by the MALI language's VM.

from vm_implementation.utils.constants import *  # pylint: disable=unused-wildcard-import
import sys

symbol_table = None
pending_set = None
is_pointer = False


class Memory:
  def __init__(self, begin):
    self.__int_slots = {}
    self.__float_slots = {}
    self.__char_slots = {}
    self.__bool_slots = {}
    self.__instance_slots = {}
    self.__pointer_slots = {}

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
    self.__pointer_begin = self.__instance_pointer_limit + 1
    self.__pointer_limit = self.__pointer_begin + BLOCK_SIZE - 1

  def set(self, address, value, assign=False):
    if self.__int_begin <= address <= self.__int_limit:
      self.__int_slots[address] = cast_value(Types.INT, value)
    elif self.__float_begin <= address <= self.__float_limit:
      self.__float_slots[address] = cast_value(Types.FLOAT, value)
    elif self.__char_begin <= address <= self.__char_limit:
      self.__char_slots[address] = cast_value(Types.CHAR, value)
    elif self.__bool_begin <= address <= self.__bool_limit:
      self.__bool_slots[address] = cast_value(Types.BOOL, value)
    elif self.__instance_pointer_begin <= address <= self.__instance_pointer_limit:
      self.__instance_slots[address] = Instance(value)
    elif self.__pointer_begin <= address <= self.__pointer_limit:
      if address in self.__pointer_slots.keys() and self.__pointer_slots[address]:
        global pending_set
        pending_set = self.__pointer_slots[address]
      else:
        self.__pointer_slots[address] = value
    else:
      raise Exception(f"Memory.Set {address}: value out of range.")

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
      return self.__instance_slots[address]
    elif self.__pointer_begin <= address <= self.__pointer_limit:
      global is_pointer
      is_pointer = True
      return self.__pointer_slots[address]
    else:
      raise Exception(f"Memory.Get {address}: value out of range.")

  def print_values(self, prefix):
    print(prefix, 'int', self.__int_slots)
    print(prefix, 'float', self.__float_slots)
    print(prefix, 'char', self.__char_slots)
    print(prefix, 'bool', self.__bool_slots)
    print(prefix, "pointer", self.__pointer_slots)
    for address, instance in self.__instance_slots.items():
      print(prefix, 'class', address)
      instance.print_instance(prefix + '\t')
    print()


class Procedure:
  def __init__(self):
    self.__vars = Memory(VAR_LOWER_LIMIT)
    self.__temps = Memory(TEMP_LOWER_LIMIT)

  def set(self, address, value):
    if VAR_LOWER_LIMIT <= address <= VAR_UPPER_LIMIT:
      self.__vars.set(address, value)
    elif TEMP_LOWER_LIMIT <= address <= TEMP_UPPER_LIMIT:
      self.__temps.set(address, value)
    else:
      raise Exception(f"Procedure.Set {address}: value out of range.")

  def get(self, address):
    if VAR_LOWER_LIMIT <= address <= VAR_UPPER_LIMIT:
      return self.__vars.get(address)
    elif TEMP_LOWER_LIMIT <= address <= TEMP_UPPER_LIMIT:
      return self.__temps.get(address)
    else:
      raise Exception(f"Procedure.Get {address}: value out of range.")

  def print_procedure(self, prefix):
    print(prefix, 'vars')
    self.__vars.print_values(prefix + '\t')
    print(prefix, 'temps')
    self.__temps.print_values(prefix + '\t')


class Instance:
  def __init__(self, class_name):
    self.__attributes = {}
    self.__attributes_stack = []
    self.__procedure_stack = []
    self.__next_procedure = None
    self.__next_attributes = None

    if class_name != '#global':
      curr_class = class_name
      while curr_class:
        self.set_attributes(curr_class)
        curr_attributes = symbol_table[curr_class]['#funcs']['#attributes']['#vars'].values(
        )
        for attribute in curr_attributes:
          value = None
          if attribute['#type'] not in raw_var_types:
            value = attribute['#type']
          if '#r' in attribute:
            for i in range(attribute['#r']):
              self.set(attribute['#address'] + i, value)
          else:
            self.set(attribute['#address'], value)
        curr_class = symbol_table[curr_class]['#parent']

      # self.__attributes_stack.append(list(self.__attributes.keys())[0])

  def set(self, address, value, assigning_param=False):
    if ATTRIBUTE_LOWER_LIMIT <= address <= ATTRIBUTE_UPPER_LIMIT:
      self.__attributes[self.__attributes_stack[-1]].set(address, value)
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      if assigning_param:
        self.__next_procedure.set(address, value)
      else:
        self.__procedure_stack[-1].set(address, value)
    else:
      raise Exception(f"Instance.Set {address}: value out of range.")

  def get(self, address):
    if ATTRIBUTE_LOWER_LIMIT <= address <= ATTRIBUTE_UPPER_LIMIT:
      for attribute in list(self.__attributes.values())[len(self.__attributes_stack)-1:]:
        value = attribute.get(address)
        if value is not None:
          return value
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      return self.__procedure_stack[-1].get(address)
    else:
      raise Exception(f"Instance.Get {address}: Value out of range.")

  def set_attributes(self, class_name):
    self.__attributes[class_name] = Memory(ATTRIBUTE_LOWER_LIMIT)
    self.__attributes_stack.append(class_name)

  def push_attributes(self, class_name):
    if top(self.__attributes_stack) != class_name:
      self.__attributes_stack.append(class_name)

  def pop_attributes(self):
    if len(self.__attributes_stack) > 1:
      self.__attributes_stack.pop()

  def prepare_new_procedure(self, class_name, func_name):
    self.__next_attributes = class_name
    self.__next_procedure = Procedure()
    var = symbol_table[class_name]['#funcs'][func_name]['#vars'].values()
    for v in var:
      value = None
      if v['#type'] not in raw_var_types:
        value = v['#type']
      if '#r' in v:
        for i in range(v['#r']):
          self.__next_procedure.set(v['#address'] + i, value)
      else:
        self.__next_procedure.set(v['#address'], value)

  def push_new_procedure(self):
    if top(self.__attributes_stack) != self.__next_attributes:
      self.__attributes_stack.append(self.__next_attributes)
    self.__procedure_stack.append(self.__next_procedure)

  def pop_procedure(self):
    self.__procedure_stack.pop()
    self.pop_attributes()

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

  def get_name(self):
    return list(self.__attributes.keys())[0]


class MemoryManager:
  def __init__(self, st):
    global symbol_table
    symbol_table = st
    self.__data_segment = Memory(DATA_LOWER_LIMIT)
    self.__constant_segment = Memory(CTE_LOWER_LIMIT)
    self.__instance_stack = [Instance('#global')]
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
      global pending_set
      if pending_set:
        new_address = pending_set
        pending_set = None
        self.set(new_address, value, assigning_param)

  def get(self, address):
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      value = self.__data_segment.get(address)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      value = self.__constant_segment.get(address)
    elif INSTANCE_LOWER_LIMIT <= address <= INSTANCE_UPPER_LIMIT:
      if self.__setting_param:
        value = self.__instance_stack[self.__depth-1].get(address)
      else:
        value = self.__instance_stack[-1].get(address)
    else:
      Error(f'Invalid address {address}.')
    global is_pointer
    if is_pointer:
      is_pointer = False
      if value:
        value = self.get(value)
    if value is None:
      Error('Segmentation Fault.')
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
    print('CURRENT INSTANCE')
    if len(self.__instance_stack):
      self.__instance_stack[-1].print_instance('\t')


class Error:
  def __init__(self, message):
    print("Error:", message)
    sys.exit()


def top(l):
  if len(l) > 0:
    return l[-1]
  return None


def cast_value(cast_type, value):
  value_type = type(value)
  if value is None:
    return None
  if cast_type == Types.INT:
    if value_type == str:
      value = float(value)
    try:
      return int(value)
    except:
      Error('Cannot cast int.')
  elif cast_type == Types.FLOAT:
    try:
      return float(value)
    except:
      Error('Cannot cast float.')
  elif cast_type == Types.CHAR:
    try:
      assert len(value) == 1
      return str(value)
    except:
      Error('Cannot cast char.')
  elif cast_type == Types.BOOL:
    try:
      return bool(value)
    except:
      Error('Cannot cast bool.')
  else:
    Error(f'Unrecognized type {cast_type}.')
