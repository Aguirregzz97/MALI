from vm_implementation.constants import *  # pylint: disable=unused-wildcard-import


class Values:
  def __init__(self):
    self.int_slots = {}
    self.float_slots = {}
    self.char_slots = {}
    self.bool_slots = {}
    self.class_slots = {}

  def set(self, address, value):
    if int_lower_limit <= address <= int_upper_limit:
      self.int_slots[address] = value
    elif float_lower_limit <= address <= float_upper_limit:
      self.float_slots[address] = value
    elif char_lower_limit <= address <= char_upper_limit:
      self.char_slots[address] = value
    elif bool_lower_limit <= address <= bool_upper_limit:
      self.bool_slots[address] = value
    elif class_lower_limit <= address <= class_upper_limit:
      self.class_slots[address] = value
    else:
      raise Exception("Valor fuera del rango de memoria de tipos")

  def get(self, address):
    if int_lower_limit <= address <= int_upper_limit:
      return self.int_slots[address]
    elif float_lower_limit <= address <= float_upper_limit:
      return self.float_slots[address]
    elif char_lower_limit <= address <= char_upper_limit:
      return self.char_slots[address]
    elif bool_lower_limit <= address <= bool_upper_limit:
      return self.bool_slots[address]
    elif class_lower_limit <= address <= class_upper_limit:
      return self.class_slots[address]
    else:
      raise Exception("Valor fuera del rango de memoria de tipos")


class Memory:
  def __init__(self):
    self.data_segment = Values()
    self.constant_segment = Values()
    self.instances = {}
    self.procedure_stack = []
    self.current_instance = None

  def set(self, address, value):
    if data_lower_limit <= address <= data_upper_limit:
      self.data_segment.set(address - data_lower_limit, value)
    elif procedure_lower_limit <= address <= procedure_upper_limit:
      self.procedure_stack[-1].set(address - procedure_lower_limit, value)
    elif class_lower_limit <= address <= class_upper_limit:
      self.current_instance = address - class_lower_limit
      self.instances[address - class_lower_limit] = Values()
    elif instance_lower_limit <= address <= class_upper_limit:
      if not self.current_instance:
        raise Exception("Instance not set")
      self.instances[self.current_instance].set(
          address - instance_lower_limit, value)
    elif cte_lower_limit <= address <= cte_upper_limit:
      self.constant_segment.set(address - cte_lower_limit, value)
    else:
      print(address)
      raise Exception("Valor fuera del rango de memorias")

  def get(self, address):
    if data_lower_limit <= address <= data_upper_limit:
      self.data_segment.get(address - data_lower_limit)
    elif procedure_lower_limit <= address <= procedure_upper_limit:
      self.procedure_stack[-1].get(address - procedure_lower_limit)
    elif class_lower_limit <= address <= class_upper_limit:
      self.current_instance = address - class_lower_limit
      # TODO delete this condition and statements
      raise Exception("q haces")
      # return self.instances[address - class_lower_limit]
    elif instance_lower_limit <= address <= class_upper_limit:
      if not self.current_instance:
        raise Exception("Instance not set")
      return self.instances[self.current_instance].get(address - instance_lower_limit)
    elif cte_lower_limit <= address <= cte_upper_limit:
      return self.constant_segment.get(address - cte_lower_limit)
    else:
      raise Exception("Valor fuera del rango de memorias")
