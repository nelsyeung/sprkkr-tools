#!/usr/bin/env python3
"""Generates compounds."""
import os
import datetime
import math
from . import nmod


def generate(settings):
    templates_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
    reps = {
        'kkrtools': {},
        'scf': {},
        'dos': {},
        'pot': {},
        'pbs': {}
    }
    now = datetime.datetime.now()
    settings['kkrtools']['created_on'] = now.strftime('%d/%m/%Y %H:%M:%S')
    elements = settings['kkrtools']['elements'].split()
    system_dir = os.path.join('generated', ''.join(elements))
    init_conc = settings['kkrtools']['concentrations'].split()
    interval = float(settings['kkrtools']['interval'])
    IT = [None]*5
    for i in range(len(elements)):
        IT[i] = nmod.find_first_line(
            os.path.join(templates_dir, 'elements.default'), elements[i])

    def create_single(concentrations):
        """Create a single system from the supplied concentrations."""
        concentrations = ['%.2f' % abs(x) for x in concentrations]
        new_dir = os.path.join(
            system_dir, '_'.join(concentrations))
        scf_inp = 'scf.inp'
        dos_inp = 'dos.inp'
        pot_inp = 'pot.pot'
        template_scf = os.path.join(templates_dir, scf_inp)
        template_dos = os.path.join(templates_dir, dos_inp)
        template_pot = os.path.join(templates_dir, pot_inp)
        new_scf = os.path.join(new_dir, scf_inp)
        new_dos = os.path.join(new_dir, dos_inp)
        new_pot = os.path.join(new_dir, pot_inp)
        dataset = ''.join(
            [i for j in zip(elements, concentrations) for i in j])
        reps['scf']['kkrtools_DATASET'] = dataset
        reps['dos']['kkrtools_DATASET'] = dataset
        reps['pot']['kkrtools_DATASET'] = dataset
        reps['pot']['kkrtools_VXC'] = settings['scf']['VXC']
        reps['pot']['kkrtools_ALG'] = settings['scf']['ALG']
        reps['pot']['kkrtools_CONC1'] = concentrations[0]
        reps['pot']['kkrtools_CONC2'] = concentrations[1]
        reps['pot']['kkrtools_CONC3'] = concentrations[2]
        reps['pot']['kkrtools_CONC4'] = concentrations[3]
        reps['pot']['kkrtools_CONC5'] = concentrations[4]
        reps['pot']['kkrtools_IT1'] = IT[0]
        reps['pot']['kkrtools_IT2'] = IT[1]
        reps['pot']['kkrtools_IT3'] = IT[2]
        reps['pot']['kkrtools_IT4'] = IT[3]
        reps['pot']['kkrtools_IT5'] = IT[4]

        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        nmod.modify_file(new_scf, template_scf, reps['scf'])
        nmod.modify_file(new_dos, template_dos, reps['dos'])
        nmod.modify_file(new_pot, template_pot, reps['pot'])

    def gen_concentrations():
        """Generate the required permutations of concentrations."""
        new_conc = init_conc.copy()
        x_range = range(math.floor((1 - float(init_conc[0])) / interval) + 1)
        y_range = range(math.floor((1 - float(init_conc[2]) -
                                    float(init_conc[4])) / interval) + 1)

        for x in x_range:
            new_conc[0] = float(init_conc[0]) + x * interval
            new_conc[1] = 1 - float(new_conc[0])

            for y in y_range:
                new_conc[2] = float(init_conc[2]) + y * interval
                new_conc[3] = 1 - new_conc[2] - float(init_conc[4])
                new_conc[4] = float(init_conc[4])

                create_single(new_conc)

    if not os.path.exists(system_dir):
        os.makedirs(system_dir)

    for block in settings:
        for setting in settings[block]:
            reps[block]['kkrtools_' + setting] = settings[block][setting]

    reps['scf'].update(reps['kkrtools'])
    reps['dos'].update(reps['kkrtools'])
    reps['pot'].update(reps['kkrtools'])

    gen_concentrations()

    reps['pbs']['kkrtools_CONC1'] = init_conc[0]
    reps['pbs']['kkrtools_CONC2'] = init_conc[1]
    reps['pbs']['kkrtools_CONC3'] = init_conc[2]
    reps['pbs']['kkrtools_CONC4'] = init_conc[3]
    reps['pbs']['kkrtools_CONC5'] = init_conc[4]
    reps['pbs']['kkrtools_TSTART'] = 1
    x_range = math.floor((1 - float(init_conc[0])) / interval) + 1
    y_range = math.floor((1 - float(init_conc[2]) -
                          float(init_conc[4])) / interval) + 1
    reps['pbs']['kkrtools_NUM'] = x_range
    reps['pbs']['kkrtools_TEND'] = x_range * y_range

    pbs_inp = 'pbs.pbs'
    new_pbs = os.path.join(system_dir, pbs_inp)
    template_pbs = os.path.join(templates_dir, pbs_inp)
    nmod.modify_file(new_pbs, template_pbs, reps['pbs'])
