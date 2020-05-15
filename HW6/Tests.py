import unittest
from unittest.mock import patch
import Task1


class Test(unittest.TestCase):
    def test_1(self):
        self.assertEqual([2, 1], Task1.func([1, 2]))

    def test_2(self):
        self.assertEqual([24, 12, 8, 6], Task1.func([1, 2, 3, 4]))

    def test_3(self):
        self.assertRaises(ValueError, Task1.func, [1])

    def test_4(self):
        self.assertRaises(TypeError, Task1.func, 1, 2, 3, 4)

    def test_5(self):
        self.assertRaises(TypeError, Task1.func, '1,2,3')

    def get_result_from_txt(self):
        with open('for_mock.txt') as f:
            return list(map(lambda x: int(x), f.read().split(',')))

    def test_6(self):
        with patch('Task1.func') as obj:
            obj.return_value = self.get_result_from_txt()

            self.assertEqual([6, 3, 2], Task1.func([1, 2]))
