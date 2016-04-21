#!/usr/bin/env python3
"""Test fileparse methods."""
import nose
import os
from kkrtools import fileparse


def test_get_settings():
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
    settings = fileparse.get_settings(inputFile)

    nose.tools.assert_equal(settings, expect)
