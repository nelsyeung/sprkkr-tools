#!/usr/bin/env python3
"""Test parser functions."""
import nose
import os
from kkrtools import parser

fixtures_dir = os.path.join('tests', 'fixtures')


def test_parse_settings_kkrtools():
    """parse_settings function parses kkrtools blocks."""
    input_file = os.path.join(fixtures_dir, 'kkrtools.inp')
    settings = parser.parse_settings(input_file)
    expect = {
        'elements': 'Mg Zn Si Sn Bi',
        'concentrations': '0.8 0.2 0.7 0.2 0.1',
        'interval': '0.1'
    }

    nose.tools.eq_(settings['kkrtools'], expect)


def test_parse_settings_scf():
    """parse_settings function parses scf blocks."""
    input_file = os.path.join(fixtures_dir, 'kkrtools.inp')
    settings = parser.parse_settings(input_file)
    expect = {
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
    }

    nose.tools.eq_(settings['scf'], expect)


def test_parse_settings_dos():
    """parse_settings function parses dos blocks."""
    input_file = os.path.join(fixtures_dir, 'kkrtools.inp')
    settings = parser.parse_settings(input_file)
    expect = {
        'NKTAB': '250',
        'NE': '200',
        'EMIN': '-0.2',
        'EMAX': '1.2',
        'ImE': '0.01'
    }

    nose.tools.eq_(settings['dos'], expect)


def test_parse_settings_pbs():
    """parse_settings function parses pbs block."""
    input_file = os.path.join(fixtures_dir, 'kkrtools.inp')
    settings = parser.parse_settings(input_file)
    expect = {
        'nodes': '1',
        'ppn': '1',
        'pvmem': '1024mb',
        'walltime': '08:00:00',
        'queue': 'taskfarm'
    }

    nose.tools.eq_(settings['pbs'], expect)
