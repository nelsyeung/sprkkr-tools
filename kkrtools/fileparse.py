#!/usr/bin/env python3
"""Parse inputs from file."""
import os
import collections


def get_settings(inputFile='kkrtools.inp'):
    """Return settings from an input file along with the defaults."""
    block = False
    supportedBlock = ['kkrtools', 'scf', 'dos']
    lineNum = 0

    settings = {
        'kkrtools': {},
        'scf': {},
        'dos': {}
    }
    templatesDir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
    defaultFile = os.path.join(templatesDir, 'kkrtools.default')

    def get_setting(line):
        """Return the setting key and value from a string line."""
        nonlocal block
        nonlocal supportedBlock
        line = line.strip()
        Setting = collections.namedtuple('Setting', ['block', 'key', 'value'])

        # Check for comments
        if not line.startswith('#'):
            # Check for start of a block
            if not block and line.startswith('%block '):
                block = line.split()[1].lower()

                # Check if block name is actually supported
                if block not in supportedBlock:
                    print('Block ' + block +
                          ' in line ' + str(lineNum) + ' not recognise')
                    block = False

            # Check for end of a block
            # This is regardless of the name
            if block is not False and line.startswith('%endblock'):
                block = False

            # If this is indeed inside a block
            # then get the key and value of the setting
            if block is not False:
                setting = line.split('=')

                if len(setting) >= 2:
                    key = setting[0].rstrip()
                    value = setting[1].lstrip()

                    # Check for comments in value
                    if '#' in value:
                        value = value.split('#')[0].rstrip()

                    return Setting(block, key, value)

        return Setting(False, False, False)

    def set_settings(inputFile, default=False):
        """Set settings from input file."""
        nonlocal lineNum

        with open(inputFile) as f:
            for line in f:
                lineNum += 1
                setting = get_setting(line)

                if (setting.block is not False and
                        # Check whether the new setting is supported
                        (default or setting.key in settings[setting.block])):
                    settings[setting.block][setting.key] = setting.value

    # First load all the defaults
    # then override it with the user inputs
    set_settings(defaultFile, True)
    set_settings(inputFile)

    return settings
