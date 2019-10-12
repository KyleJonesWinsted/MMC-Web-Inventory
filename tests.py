import unittest

import data_controller as db

class TestDataModel(unittest.TestCase):
    
    def test_get_item_by_sku(self):
        test_item = db.Item(sku = 999, part_no = 'test part', manufacturer = 'test manufacturer', description = 'test description')
        db.session.add(test_item)
        result_item = db.get_item_by_sku(999)
        self.assertIs(test_item, result_item)
        db.session.rollback()

if __name__ == '__main__':
    unittest.main()