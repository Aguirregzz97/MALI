from vm_implementation.utils.constants import *  # pylint: disable=unused-wildcard-import


class Values:
  def __init__(self):
    self.__int_slots = {}
    self.__float_slots = {}
    self.__char_slots = {}
    self.__bool_slots = {}
    self.__class_slots = {}

  def set(self, address, value):
    if INT_LOWER_LIMIT <= address <= INT_UPPER_LIMIT:
      self.__int_slots[address] = value
    elif FLOAT_LOWER_LIMIT <= address <= FLOAT_UPPER_LIMIT:
      self.__float_slots[address] = value
    elif CHAR_LOWER_LIMIT <= address <= CHAR_UPPER_LIMIT:
      self.__char_slots[address] = value
    elif BOOL_LOWER_LIMIT <= address <= BOOL_UPPER_LIMIT:
      self.__bool_slots[address] = value
    elif CLASS_LOWER_LIMIT <= address <= CLASS_UPPER_LIMIT:
      self.__class_slots[address] = value
    else:
      raise Exception(
          f"Set {address}: Valor fuera del rango de memoria de tipos")

  def get(self, address):
    if INT_LOWER_LIMIT <= address <= INT_UPPER_LIMIT:
      return self.__int_slots[address]
    elif FLOAT_LOWER_LIMIT <= address <= FLOAT_UPPER_LIMIT:
      return self.__float_slots[address]
    elif CHAR_LOWER_LIMIT <= address <= CHAR_UPPER_LIMIT:
      return self.__char_slots[address]
    elif BOOL_LOWER_LIMIT <= address <= BOOL_UPPER_LIMIT:
      return self.__bool_slots[address]
    elif CLASS_LOWER_LIMIT <= address <= CLASS_UPPER_LIMIT:
      return self.__class_slots[address]
    else:
      raise Exception(
          f"Get {address}: Valor fuera del rango de memoria de tipos")

  def print_values(self):
    print('int', self.__int_slots)
    print('float', self.__float_slots)
    print('char', self.__char_slots)
    print('bool', self.__bool_slots)
    print('class', self.__class_slots)
    print()


class Memory:
  def __init__(self, symbol_table):
    self.__data_segment = Values()
    self.__constant_segment = Values()
    self.__instances = {}
    self.__procedure_stack = []
    self.__symbol_table = symbol_table
    self.__current_instance = None

  def set(self, address, value):
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      self.__data_segment.set(address - DATA_LOWER_LIMIT, value)
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      self.__procedure_stack[-1].set(address - PROCEDURE_LOWER_LIMIT, value)
    elif CLASS_LOWER_LIMIT <= address <= CLASS_UPPER_LIMIT:
      self.__current_instance = address - CLASS_LOWER_LIMIT
      self.__instances[address - CLASS_LOWER_LIMIT] = Values()
    elif INSTANCE_LOWER_LIMIT <= address <= INSTANCE_UPPER_LIMIT:
      if not self.__current_instance:
        raise Exception("Instance not set")
      self.__instances[self.__current_instance].set(
          address - INSTANCE_LOWER_LIMIT, value)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      self.__constant_segment.set(address - CTE_LOWER_LIMIT, value)
    else:
      raise Exception(f"Set {address}: valor fuera del rango de memorias")

  def get(self, address):
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      return self.__data_segment.get(address - DATA_LOWER_LIMIT)
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      return self.__procedure_stack[-1].get(address - PROCEDURE_LOWER_LIMIT)
    elif CLASS_LOWER_LIMIT <= address <= CLASS_UPPER_LIMIT:
      self.__current_instance = address - CLASS_LOWER_LIMIT
      # TODO delete this condition and statements
      raise Exception("q haces")
      # return self.__instances[address - class_LOWER_LIMIT]
    elif INSTANCE_LOWER_LIMIT <= address <= INSTANCE_UPPER_LIMIT:
      if not self.__current_instance:
        raise Exception("Instance not set")
      return self.__instances[
          self.__current_instance].get(address - INSTANCE_LOWER_LIMIT)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      return self.__constant_segment.get(address - CTE_LOWER_LIMIT)
    else:
      raise Exception(f"Get {address}: valor fuera del rango de memorias")

  def new_procedure(self, class_name, func_name):
    if func_name == 'init':
      self.__instances[self.__current_instance] = Values()
      values = self.__instances[self.__current_instance]
    else:
      self.__procedure_stack.append(Values())
      values = self.__procedure_stack[-1]

    vars = self.__symbol_table[class_name]['#funcs'][func_name]['#vars'].values(
    )
    for var in vars:
      values.set(var['#address'] - PROCEDURE_LOWER_LIMIT, None)
