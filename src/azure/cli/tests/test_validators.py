import unittest
from six import StringIO

from azure.cli.commands.validators import * # pylint: disable=wildcard-import, unused-wildcard-import

class Test_storage_validators(unittest.TestCase):

    def setUp(self):
        self.io = StringIO()

    def tearDown(self):
        self.io.close()

    def test_key_value_pairs_valid(self):
        the_input = 'a=b;c=d'
        actual = validate_key_value_pairs(the_input)
        expected = {'a':'b', 'c':'d'}
        self.assertEqual(actual, expected)

    def test_key_value_pairs_invalid(self):
        the_input = 'a=b;c=d;e'
        actual = validate_key_value_pairs(the_input)
        expected = {'a':'b', 'c':'d'}
        self.assertEqual(actual, expected)

    def test_tags_valid(self):
        the_input = 'a=b;c=d;e'
        actual = validate_tags(the_input)
        expected = {'a':'b', 'c':'d', 'e':''}
        self.assertEqual(actual, expected)

    def test_tags_invalid(self):
        the_input = ''
        actual = validate_tags(the_input)
        expected = {}
        self.assertEqual(actual, expected)

    def test_tag(self):
        self.assertEqual(validate_tag('test'), {'test':''})
        self.assertEqual(validate_tag('a=b'), {'a':'b'})
        self.assertEqual(validate_tag('a=b;c=d'), {'a':'b;c=d'})

if __name__ == '__main__':
    unittest.main()
