#!/usr/bin/env python3
"""Test fileparse methods."""
import unittest
import os
from kkrtools import fileparse


class TestFileparseMethods(unittest.TestCase):
    """Test fileparse methods."""

    def test_getSettings(self):
        """
        Test whether getSettings method
        get settings from an input file along with the defaults.
        """
        inputFile = os.path.join('tests', 'fixtures', 'kkrtools.inp')
        expect = {
            'kkrtools': {},
            'scf': {
                'VXC': 'VBH',
                'ALG': 'BROYDEN2',
                'NITER': '250',
                'MIX': '0.2'
            },
            'dos': {
                'NE': '200',
                'EMIN': '-0.2',
                'EMAX': '1.2',
                'ImE': '0.01'
            }
        }
        settings = fileparse.getSettings(inputFile)

        self.assertEqual(settings, expect)

if __name__ == '__main__':
    unittest.main()
