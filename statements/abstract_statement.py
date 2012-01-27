#!/usr/bin/python

class StatementInitError(Exception):
  """Represents a basic assertion failure on the object."""   

class AbstractStatement(object):
  """Represents an abstract statement object."""

  def __init__(self, filetext):
    """Loads the filetext into the superclass."""
    if not filetext:
      raise StatementInitError('Invalid statement')
    self.filetext = filetext
    self.filelines = filetext.split('\n')

  @property
  def transactions(self):
    raise NotImplementedError

  @property
  def total_amount(self):
    total = 0.0
    for item_dict in self.transactions:
      total += item_dict['amount']
    return total

  def print_stmt(self):
    raise NotImplementedError
    
