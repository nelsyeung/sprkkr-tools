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
    input_file = os.path.join('tests', 'fixtures', 'kkrtools.inp')
    expect = {
        'kkrtools': {
            'elements': 'Mg Zn Si Sn Bi',
            'concentrations': '0.8 0.2 0.7 0.2 0.1',
            'interval': '0.1'
        },
        'scf': {
            'NKTAB': '250',
            'NE': '30',
            'EMIN': '-0.2',
            'ImE': '0.0',
            'NITER': '250',
            'MIX': '0.2',
            'VXC': 'VBH',
            'TOL': '0.00001',
            'ISTBRY': '1',
            'ALG': 'BROYDEN2'
        },
        'dos': {
            'NKTAB': '250',
            'NE': '200',
            'EMIN': '-0.2',
            'EMAX': '1.2',
            'ImE': '0.01'
        }
    }
    settings = fileparse.get_settings(input_file)

    nose.tools.assert_equal(settings, expect)
