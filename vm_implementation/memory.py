# Memomry structure used by the MALI language's VM.

from vm_implementation.utils.memory_utils import *  # pylint: disable=unused-wildcard-import
from vm_implementation.utils.constants import *  # pylint: disable=unused-wildcard-import

pending_to_set = None
'''Used to assign pointers.'''

is_pointer = False
'''True when get returns a pointer.'''


class Memory:
  '''Stores values with their address.'''

  def __init__(self, adjust: int):
    self.__int_slots = {}
    '''Memory slots for int values.'''

    self.__float_slots = {}
    '''Memory slots for float values.'''

    self.__char_slots = {}
    '''Memory slots for char values.'''

    self.__bool_slots = {}
    '''Memory slots for bool values.'''

    self.__instance_slots = {}
    '''Memory slots for instance values.'''

    self.__pointer_slots = {}
    '''Memory slots for pointer values.'''

    self.__address_adjust = adjust
    '''Address adjustment for the memory block.'''

  def set(self, unadjusted_address: int, value, assign=False):
    '''Set given address with given value.

    Find value type by the address and save it in the corresponding slot.
    '''
    address = unadjusted_address - self.__address_adjust
    if INT_LOWER_LIMIT <= address <= INT_UPPER_LIMIT:
      self.__int_slots[address] = cast_value(Types.INT, value)
    elif FLOAT_LOWER_LIMIT <= address <= FLOAT_UPPER_LIMIT:
      self.__float_slots[address] = cast_value(Types.FLOAT, value)
    elif CHAR_LOWER_LIMIT <= address <= CHAR_UPPER_LIMIT:
      self.__char_slots[address] = cast_value(Types.CHAR, value)
    elif BOOL_LOWER_LIMIT <= address <= BOOL_UPPER_LIMIT:
      self.__bool_slots[address] = cast_value(Types.BOOL, value)
    elif CLASS_LOWER_LIMIT <= address <= CLASS_UPPER_LIMIT:
      self.__instance_slots[address] = Instance()
    elif POINTER_LOWER_LIMIT <= address <= POINTER_UPPER_LIMIT:
      if address in self.__pointer_slots.keys() and self.__pointer_slots[address]:
        global pending_to_set
        pending_to_set = self.__pointer_slots[address]
      else:
        self.__pointer_slots[address] = value
    else:
      raise Exception(
          f"Memory.Set {address, unadjusted_address}: value out of range.")

  def get(self, unadjusted_address: int, printable=False):
    '''Get value stored in given address

    Finds value type by the address and searches for the value in the
    corresponding type slot.

    Returns value.
    '''
    address = unadjusted_address - self.__address_adjust
    if INT_LOWER_LIMIT <= address <= INT_UPPER_LIMIT:
      return self.__int_slots.get(address, None)
    elif FLOAT_LOWER_LIMIT <= address <= FLOAT_UPPER_LIMIT:
      return self.__float_slots.get(address, None)
    elif CHAR_LOWER_LIMIT <= address <= CHAR_UPPER_LIMIT:
      if printable:
        return chr(self.__char_slots.get(address, 0))
      return self.__char_slots.get(address, None)
    elif BOOL_LOWER_LIMIT <= address <= BOOL_UPPER_LIMIT:
      if printable:
        return bool(self.__bool_slots.get(address, None))
      return self.__bool_slots.get(address, None)
    elif CLASS_LOWER_LIMIT <= address <= CLASS_UPPER_LIMIT:
      return self.__instance_slots.get(address, None)
    elif POINTER_LOWER_LIMIT <= address <= POINTER_UPPER_LIMIT:
      global is_pointer
      is_pointer = True
      return self.__pointer_slots[address]
    else:
      raise Exception(
          f"Memory.Get {address, unadjusted_address}: value out of range.")

  def print_memory(self, prefix):
    '''Print memory for debugging.'''
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
  '''Structure of a function/method.'''

  def __init__(self):
    self.__vars = Memory(VAR_LOWER_LIMIT)
    '''Stores procedure variables.'''

    self.__temps = Memory(TEMP_LOWER_LIMIT)
    '''Stores procedure temporals.'''

  def set(self, address: int, value):
    '''Set given address to given value.

    Determines wheter the address is a variable or a temporal, and calls set on
    the corresponding memory.
    '''
    if VAR_LOWER_LIMIT <= address <= VAR_UPPER_LIMIT:
      self.__vars.set(address, value)
    elif TEMP_LOWER_LIMIT <= address <= TEMP_UPPER_LIMIT:
      self.__temps.set(address, value)
    else:
      raise Exception(f"Procedure.Set {address}: value out of range.")

  def get(self, address: int, printable=False):
    '''Get value stored on a given address.

    Determines wheter the address is a variable or a temporal, and calls get on
    the corresponding memory.
    '''
    if VAR_LOWER_LIMIT <= address <= VAR_UPPER_LIMIT:
      return self.__vars.get(address, printable)
    elif TEMP_LOWER_LIMIT <= address <= TEMP_UPPER_LIMIT:
      return self.__temps.get(address, printable)
    else:
      raise Exception(f"Procedure.Get {address}: value out of range.")

  def print_procedure(self, prefix):
    '''Print procedure for debugging.'''
    print(prefix, 'temps')
    self.__temps.print_memory(prefix + '\t')
    print(prefix, 'vars')
    self.__vars.print_memory(prefix + '\t')


class Instance:
  '''Structure of a class intance.'''

  def __init__(self):
    self.__attributes = Memory(ATTRIBUTE_LOWER_LIMIT)

    self.__procedure_stack = []
    '''Instance of Procdure. Keep track of procedure calls.'''

    self.__next_procedure = None
    '''Instance of the next Procedure. Assigned on ERA and pushed to
       procedure_stack on GOSUB.'''

  def set(self, address: int, value, assigning_param=False):
    '''Set given address to given value.

    Determines wheter the address is an attribute or a variable from a
    procedure, and calls set on the corresponding memory.
    '''
    if ATTRIBUTE_LOWER_LIMIT <= address <= ATTRIBUTE_UPPER_LIMIT:
      self.__attributes.set(address, value)
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      if assigning_param:
        self.__next_procedure.set(address, value)
      else:
        self.__procedure_stack[-1].set(address, value)
    else:
      raise Exception(f"Instance.Set {address}: value out of range.")

  def get(self, address: int, printable=False):
    '''Get value stored on a given address.

    Determines wheter the address is an attribute or a variable from a
    procedure, and calls get on the corresponding memory.
    '''
    if ATTRIBUTE_LOWER_LIMIT <= address <= ATTRIBUTE_UPPER_LIMIT:
      return self.__attributes.get(address, printable)
    elif PROCEDURE_LOWER_LIMIT <= address <= PROCEDURE_UPPER_LIMIT:
      return self.__procedure_stack[-1].get(address, printable)
    else:
      raise Exception(f"Instance.Get {address}: Value out of range.")

  def prepare_new_procedure(self, class_name: str, func_name: str):
    '''Creates a new procedure.

    Called by ERA. Keeps procedure on aux var until GOSUB is called.
    '''
    self.__next_procedure = Procedure()

  def push_new_procedure(self):
    '''Pushes next procedure to procedure stack.

    Called by GOSUB.
    '''
    self.__procedure_stack.append(self.__next_procedure)

  def pop_procedure(self):
    '''Pops procedure from procedure stack.

    Called by ENDPROC.
    '''
    self.__procedure_stack.pop()

  def print_instance(self, prefix):
    '''Print Instance for debugging.'''
    self.__attributes.print_memory(prefix + '\t')
    prefix += '\t'
    for procedure in self.__procedure_stack:
      procedure.print_procedure(prefix)
    if self.__next_procedure:
      print(prefix, 'next procedure')
      self.__next_procedure.print_procedure(prefix)


class MemoryManager:
  '''Provides methods for Memory management.'''

  def __init__(self):
    self.__data_segment = Memory(DATA_LOWER_LIMIT)
    '''Instance of Memory with global variables.'''

    self.__constant_segment = Memory(CTE_LOWER_LIMIT)
    '''Instance of Memory with constant values'''

    self.__instance_stack = [Instance()]
    '''Stack of Instance instances.'''

    self.__return = None
    '''Saves value returned by function.'''

    self.setting_param = False
    '''If true, sets values on next_procedure.'''

    self.__depth = 0
    '''Counter. Accumulates on ENTER_INSTANCE and decreases on EXIT_INSTANCE.
       Used to check which instance originated the call.'''

    # Prepare memory to begin running program.
    self.prepare_new_procedure('#global', '#main')
    self.push_new_procedure()
    self.__depth = 0

  def set(self, address: int, value, assigning_param=False):
    '''Set given address to given value.

    Determines wheter the address is a global variable, constant value, or
    comes from an instance, and calls set on the corresponding memory.
    '''
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      self.__data_segment.set(address, value)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      self.__constant_segment.set(address, value)
    else:
      if self.setting_param and not assigning_param:
        self.__instance_stack[self.__depth-1].set(address, value)
      else:
        self.__instance_stack[-1].set(address, value, self.setting_param)
      global pending_to_set
      if pending_to_set:
        new_address = pending_to_set
        pending_to_set = None
        self.set(new_address, value, assigning_param)

  def get(self, address: int, printable=False, validate=True):
    '''Get value stored on a given address.

    Determines wheter the address is a global variable, constant value, or
    comes from an instance, and calls get on the corresponding memory.
    '''
    if DATA_LOWER_LIMIT <= address <= DATA_UPPER_LIMIT:
      value = self.__data_segment.get(address, printable)
    elif CTE_LOWER_LIMIT <= address <= CTE_UPPER_LIMIT:
      value = self.__constant_segment.get(address, printable)
    elif INSTANCE_LOWER_LIMIT <= address <= INSTANCE_UPPER_LIMIT:
      if self.setting_param:
        value = self.__instance_stack[self.__depth-1].get(address, printable)
      else:
        value = self.__instance_stack[-1].get(address, printable)
    else:
      Error(f'Invalid address {address}.')
    global is_pointer
    if is_pointer:
      is_pointer = False
      if value:
        value = self.get(value)
    if value is None and validate:
      Error('Accessing unassigned memory space.')
    return value

  def push_instance(self, address: int, class_name: str):
    '''Appends a new instance to the instance stack.'''
    self.__depth -= 1
    instance = self.get(address, validate=False)
    if not instance:
      self.set(address, None)
      instance = self.get(address)
    self.__instance_stack.append(instance)

  def pop_instance(self):
    '''Pops instance from the instance stack.'''
    if self.__depth < 0:
      self.__depth += 1
    self.__instance_stack.pop()

  def prepare_new_procedure(self, class_name: str, func_name: str):
    '''Calls prepare_new_procedure() on current instance.'''
    self.__instance_stack[-1].prepare_new_procedure(class_name, func_name)

  def push_new_procedure(self):
    '''Calls push_new_procedure() on current instance.'''
    self.__depth = 0
    self.__instance_stack[-1].push_new_procedure()

  def pop_procedure(self):
    '''Calls pop_new_procedure() on current instance.'''
    self.__instance_stack[-1].pop_procedure()

  def set_return(self, value):
    '''Sets return to given value.'''
    self.__return = value

  def get_return(self):
    '''Returns last returned value.'''
    return_val = self.__return
    self.__return = None
    return return_val

  def print(self):
    '''Print MemoryManager for debugging.'''
    print('Data segment')
    self.__data_segment.print_memory('\t')
    print('Constant segment')
    self.__constant_segment.print_memory('\t')
    print('Instances')
    for instance in self.__instance_stack:
      print('-------------------------')
      instance.print_instance('\t')
