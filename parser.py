#!/usr/bin/python


import logging as log
import sys
import traceback
from statements import mbna as s

def open_file(filename):
  """Opens the file given by filename, and returns the result as a string.
  Args:
    filename (str): Name of the file to open, either absolute or relative path.
  Returns:
    (str) the contents of the file.
  """
  try:
    f = open(filename)
    try:
      text = f.read()
    finally:
      f.close()
  except IOError:
    traceback.print_exc()
    raise 
  return text

def help():
  """Prints a help message."""
  print 'Usage: %s <path to statement.txt>' % sys.argv[0]

def main():
  log.basicConfig(level=log.INFO,
                  format='%(asctime)s %(levelname)s: %(message)s',
                  datefmt='%Y-%m-%d %H:%M:%S')   
  if len(sys.argv) <= 1:
    help()
    sys.exit(1)
  log.info('Starting the program. Opening: %s', sys.argv[1])
  text = open_file(sys.argv[1])        
  stmt = s.MbnaStatement(text)

  stmt.printstmt()
  log.info('***** DONE: %d transactions with a total value of: $%.2f *****', 
           len(stmt.transactions), stmt.total_amount)
  log.info('Completed successfully.')


if __name__ == '__main__':
  main()    
