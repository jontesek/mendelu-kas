#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import unittest

from src.Sha1Algo import Sha1Algo


class TestSha1Algo(unittest.TestCase):

    def setUp(self):
        self.sa = Sha1Algo()

    # Test methods

    def test_string_1(self):
        digests = self._general_string_test('A test')
        self.assertEqual(digests[0], digests[1])

    def test_string_2(self):
        digests = self._general_string_test('Příliš žluťoučký kůň úpěl ďábelské ódy')
        self.assertEqual(digests[0], digests[1])

    def test_file_1(self):
        digests = self._general_file_test('tests/h_file.txt')
        self.assertEqual(digests[0], digests[1])

    def test_file_2(self):
        digests = self._general_file_test('tests/h_file.pdf')
        self.assertEqual(digests[0], digests[1])

    # General methods for testing

    def _general_string_test(self, text):
        # Sha1Algo
        digest1 = self.sa.hash_text(text)
        # HashLib
        hasher = hashlib.sha1()
        my_str = unicode(text, 'utf-8').encode('utf-8')
        hasher.update(my_str)
        digest2 = hasher.hexdigest()
        # result
        return [digest1, digest2]

    def _general_file_test(self, file_path):
        # Sha1Algo
        digest1 = self.sa.hash_file(file_path)
        # HashLib
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as file_obj:
            hasher.update(file_obj.read())
        digest2 = hasher.hexdigest()
        # result
        return [digest1, digest2]


# Run tests when the file is run from terminal.
if __name__ == '__main__':
    unittest.main()
