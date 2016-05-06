#!/usr/bin/env python3
"""Test gencomp functions."""
import nose
import os
import shutil
from kkrtools import gencomp

fixtures_dir = os.path.join('tests', 'fixtures')


def setup_pass():
    pass


def teardown_generated():
    """Tear down generated fixtures."""
    shutil.rmtree('generated')


@nose.with_setup(setup_pass, teardown_generated)
def test_parse_settings():
    """Test generate function."""
    settings = {
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

    gencomp.generate(settings)

    conc = [None] * 5

    for i in range(3):
        conc[0] = str('%.2f' % abs(0.8 + i * 0.1))
        conc[1] = str('%.2f' % abs(1.0 - float(conc[0])))

        for j in range(3):
            conc[2] = str('%.2f' % abs(0.7 + j * 0.1))
            conc[3] = str('%.2f' % abs(1.0 - float(conc[2]) - 0.1))
            conc[4] = str('%.2f' % abs(0.1))

            dirname = os.path.join('generated', 'MgZnSiSnBi', 'new',
                                   '_'.join(conc))
            scf = os.path.join(dirname, 'scf.inp')
            dos = os.path.join(dirname, 'dos.inp')
            pot = os.path.join(dirname, 'pot.pot')

            nose.tools.ok_(os.path.isdir(dirname), dirname + ' missing')
            nose.tools.ok_(os.path.exists(scf), scf + ' missing')
            nose.tools.ok_(os.path.exists(dos), dos + ' missing')
            nose.tools.ok_(os.path.exists(pot), pot + ' missing')
