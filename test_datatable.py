# coding: utf-8

import unittest
from copa_transparente import *

class DataTableTest(unittest.TestCase):
  def setUp(self): # qd estoura exception aki teardown nao eh executado
    self.addCleanup(self.my_cleanup, ('Cleanup executado')) # a nao ser q vc force um metodo custom
    self.table = DataTable('A')
  def my_cleanup(self, msg):
    print(msg)
  def test_add_column(self):
    self.assertEqual(0, len(self.table._columns))
    self.table.add_column('BId','bigint')
    self.assertEqual(1, len(self.table._columns))
    self.table.add_column('value','numeric')
    self.assertEqual(2, len(self.table._columns))
    self.table.add_column('desc','varchar')
    self.assertEqual(3, len(self.table._columns))
  def test_add_column_invalid_type(self):
    self.assertRaises(Exception,self.table.add_column,('col','invalid'))
  def tearDown(self): # nunca executa qd setup da erro
    print('tearDown executado')

if __name__ == '__main__':
  unittest.main()
