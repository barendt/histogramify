#!/usr/bin/env python

import os
from random import choice
from string import letters, digits
import unittest

from histogramifier import *


class TestSetupOfHistogramifier(unittest.TestCase):
    def test_it_fails_with_nonexistent_file(self):
        file_path = "".join([choice(letters + digits) for i in range(15)])
        h = Histogramifier(file_path)         
        try:
            h.histogramify()
            self.fail()
        except HistogramifierFileNotFoundError:
            pass

    def test_it_detects_known_filetypes(self):
        files = ("foo.csv", "foo.xls")
        for file_path in files:
            h = Histogramifier(file_path)
            h.detect_file_type()
            self.assertEqual(h.file_type, file_path.split(".")[-1])
    
    def test_it_fails_with_unknown_filetypes(self):
        file_path = "foo.foo"
        h = Histogramifier(file_path)
        try:
            h.detect_file_type()
            self.fail()
        except HistogramifierUnprocessableFileError:
            pass

    def test_it_correctly_sets_an_output_path(self):
        file_path = "test.csv"
        h = Histogramifier(file_path)
        h.histogramify()
        self.assertEqual('test.png', h.output_file_path)

class TestLoadingOfData(unittest.TestCase):
    def test_it_can_load_from_csv(self):
        h = Histogramifier('test.csv')
        h.histogramify()
        self.assertEqual(11, len(h.data))

    def test_it_can_load_from_xls(self):
        h = Histogramifier('test.xls')
        h.histogramify()
        self.assertEqual(11, len(h.data))

if __name__ == '__main__':    
    unittest.main()
