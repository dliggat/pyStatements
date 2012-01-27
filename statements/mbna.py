#!/usr/bin/python

import calendar
import re
import unittest
import abstract_statement


def is_numeric(value):
  """A helper function to determine if a value is numeric."""
  try:
    float(value)
    return True
  except (ValueError, TypeError):
    return False

def date_tuple(value):
  """A helper function to return the date of a transaction.
  Args:
    value (str): A date string in the form '02/17'.
  Returns:
    (tuple): The date values.
  """
  p = re.compile(r'\d{2}/\d{2}')
  if not p.match(value):
    raise InvalidArgError('Argument not of the appropriate form')

  month_int, day_int = [int(_) for _ in value.split('/')]
  month = calendar.month_name[month_int]
  day = str(day_int)
  year = '2011'  # TODO: Fix this. Probably should parse the file.
  return (year, month, day)


class InvalidArgError(Exception):
  """Represents an invalid argument."""

class MbnaStatement(abstract_statement.AbstractStatement):
  """An object to represent an MBNA text statement."""

  def __init__(self, filetext):
    """Initialize function.
    Args:
      filetext (str): The text of a statement file.
    """
    super(MbnaStatement, self).__init__(filetext)
    self._trnx_list = []

  @property
  def transactions(self):
    """Returns the transaction related rows.
    Returns:
      (list) The transactions that were found in the file.
    """
    if self._trnx_list:
      return self._trnx_list
    p = re.compile(r"""
      ^\s{7}                               # Start the line then 7 spaces.
      (?P<transaction_date>\d{2}/\d{2})    # Two digits, forward slash, two digits.
      \s{7}                                # 7 spaces.
      (?P<posted_date>\d{2}/\d{2})         # Two digits, forward slash, two digits.
      \s{3}                                # 3 spaces.
      (?P<establishment>.+[\w-])           # Anything (incl spaces) plus a trailing printable character.
      \s+?                                 # Whitespace.
      (?P<city>[\w-]+)                     # Only printable characters (safe assumption?).
      \s+?                                 # Whitespace.
      (?P<stateprov>[A-Z]{2})              # Two uppercase letters (e.g. BC, CA).
      \s+?                                 # Whitespace. 
      (?P<ref_num>\d{4})                   # Four digits.
      \s+?                                 # Whitespace.
      (?P<acct_num>\d{4})                  # Four digits.
      \s+?                                 # Whitespace.
      \$(?P<amount>[\d.]+)                 # A dollar sign followed by a floating point number.
      $                                    # Now at the end of the line.
      """, re.VERBOSE)                     # Verbose allows the regex itself to ignore whitespace so we can span lines. 
    

    for line in self.filelines:
      m = p.match(line)
      if m:
        items = {}
        year, month, day = date_tuple(m.group('posted_date'))
        items['posted_year'] = year 
        items['posted_month'] = month
        items['posted_day'] = day
        items['transaction_date'] = m.group('transaction_date')
        items['establishment'] = m.group('establishment')
        items['city'] = m.group('city')
        items['stateprov'] = m.group('stateprov')
        items['ref_num'] = int(m.group('ref_num'))
        items['acct_num'] = int(m.group('acct_num'))
        items['amount'] = float(m.group('amount'))
        self._trnx_list.append(items)

    return self._trnx_list
  

  def printstmt(self, sep='; '):
    headings = ['posted_year', 
                'posted_month', 
                'posted_day', 
                'transaction_date', 
                'establishment', 
                'city', 
                'stateprov', 
                'ref_num', 
                'acct_num', 
                'amount']
    li = []
    li.append(sep.join(headings))
    for item_dict in self.transactions:
      order_li = [item_dict[headings[0]],
                  item_dict[headings[1]],
                  item_dict[headings[2]],
                  item_dict[headings[3]],
                  item_dict[headings[4]],
                  item_dict[headings[5]],
                  item_dict[headings[6]],
                  item_dict[headings[7]],
                  item_dict[headings[8]],
                  item_dict[headings[9]]]
      s = sep.join([str(_) for _ in order_li])
      li.append(s)

    print "\n".join(li)


class TestHelpers(unittest.TestCase):

  def testPositiveIsNumeric(self):
    self.assertTrue(is_numeric(3))
    self.assertTrue(is_numeric(3.3))
    self.assertTrue(is_numeric(-1))
    self.assertTrue(is_numeric(0))
    self.assertTrue(is_numeric('2.121'))

  def testNegativeIsNumeric(self):
    self.assertFalse(is_numeric('3f'))
    self.assertFalse(is_numeric(''))
    self.assertFalse(is_numeric(None))

  def testDateTuple(self):
    result = date_tuple('12/13')
  def testDateTupleRaises(self):
    self.failUnlessRaises(InvalidArgError, date_tuple, 'not a valid input')

class TestMbnaStatement(unittest.TestCase):
  """Tests the MbnaStatement class."""

  file_contents = None

  def setUp(self):
    if self.__class__.file_contents is None:
      f = open('mbna_sample_input.txt')
      self.__class__.file_contents = f.read()
      f.close()

  def testFailInitializeWithEmpty(self):
    self.failUnlessRaises(abstract_statement.StatementInitError, MbnaStatement, '')

  def testContents(self):
    obj = MbnaStatement(self.__class__.file_contents)
    self.assertEqual(len(obj.transactions), 35)
    self.assertAlmostEqual(obj.total_amount, 966.03)  # Because these are floats.


if __name__ == '__main__':
  unittest.main()


