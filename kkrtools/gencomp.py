#!/usr/bin/env python3
"""Generates compounds."""
import os
import math
from decimal import getcontext, Decimal
from datetime import datetime
from . import nmod


def generate(settings):
    templates_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'templates')

    settings['pot'] = {
        'VXC': settings['scf']['VXC'],
        'ALG': settings['scf']['ALG']
    }

    now = datetime.now()
    settings['kkrtools']['created_on'] = now.strftime('%d/%m/%Y %H:%M:%S')

    elements = settings['kkrtools']['elements'].split()
    sys_dir = os.path.join('generated', ''.join(elements))
    sys_new_dir = os.path.join(sys_dir, 'new')

    if not os.path.exists(sys_new_dir):
        os.makedirs(sys_new_dir)

    init_conc = settings['kkrtools']['concentrations'].split()
    precision = 2
    for i in range(len(init_conc)):
        precision = max(precision, len(init_conc[i].split('.')[1]) + 1)
        init_conc[i] = Decimal(init_conc[i])
    getcontext().prec = precision
    interval = Decimal(settings['kkrtools']['interval'])
    num_generated = 0

    # Export shared settings from kkrtools block across all the blocks.
    shared_settings = ['created_on']
    for block in settings:
        for setting in shared_settings:
            settings[block][setting] = settings['kkrtools'][setting]

    # Get all the elements details
    for i in range(len(elements)):
        settings['pot']['IT' + str(i+1)] = nmod.find_first_line(
            os.path.join(templates_dir, 'elements.default'), elements[i])

    # Initialise replacements variables
    reps = {'pot': {}}
    for block in settings:
        if block not in reps:
            reps[block] = {}

        for setting in settings[block]:
            reps[block]['kkrtools_' + setting] = settings[block][setting]

    def generate_single(concentrations):
        """Create a single system from the supplied concentrations."""
        concentrations = ['%.2f' % abs(x) for x in concentrations]
        dirname = '_'.join(concentrations)
        new_dir = os.path.join(sys_new_dir, dirname)
        inp_files = ['scf.inp', 'dos.inp', 'pot.pot']
        templates, new_files = {}, {}

        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        for i in range(len(elements)):
            reps['pot']['kkrtools_CONC' + str(i+1)] = concentrations[i]

        for inp_file in inp_files:
            inp_type = inp_file.split('.')[0]
            templates[inp_type] = os.path.join(templates_dir, inp_file)
            new_files[inp_type] = os.path.join(new_dir, inp_file)

            # Set up dataset to be the element followed by its concentration.
            reps[inp_type]['kkrtools_DATASET'] = ''.join(
                [i for j in zip(elements, concentrations) for i in j])

            nmod.modify_file(
                templates[inp_type], new_files[inp_type], reps[inp_type])

        with open(os.path.join(sys_dir, 'kkrtools-dirs.txt'), 'a') as f:
            f.write(dirname + '\n')

    def gen_concentrations():
        """Generate the required permutations of concentrations."""
        nonlocal num_generated
        new_conc = init_conc.copy()
        x_range = range(math.floor((1 - init_conc[0]) / interval) + 1)
        y_range = range(math.floor((1 - init_conc[2] - init_conc[4]) /
                                   interval) + 1)

        for x in x_range:
            new_conc[0] = init_conc[0] + x * interval
            new_conc[1] = 1 - new_conc[0]

            for y in y_range:
                new_conc[2] = init_conc[2] + y * interval
                new_conc[3] = 1 - new_conc[2] - init_conc[4]
                new_conc[4] = init_conc[4]

                generate_single(new_conc)

                num_generated += 1

    gen_concentrations()

    reps['pbs']['kkrtools_t'] = num_generated

    pbs_inp = 'pbs.pbs'
    new_pbs = os.path.join(sys_dir, pbs_inp)
    template_pbs = os.path.join(templates_dir, pbs_inp)
    nmod.modify_file(template_pbs, new_pbs, reps['pbs'])
