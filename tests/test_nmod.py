#!/usr/bin/env python3
"""Test nmod functions."""
import os
import pytest
from kkrtools import nmod

fixtures_dir = os.path.join('tests', 'fixtures')


@pytest.fixture
def rmnew(request):
    """Remove nmod.new"""
    newfile = os.path.join(fixtures_dir, 'nmod.new')

    def fin():
        os.remove(newfile)

    request.addfinalizer(fin)


def test_replace_text():
    """Test replace_text function."""
    text = 'Hello kkrtools_name. NE should be kkrtools_NE.'
    reps = {
        'kkrtools_name': 'Nelson',
        'kkrtools_NE': '200'
    }
    text = nmod.replace_text(text, reps)
    expect = 'Hello Nelson. NE should be 200.'

    assert text == expect


def test_find_first_line():
    """Test find_first_line function."""
    filepath = os.path.join(fixtures_dir, 'nmod.inp')
    string = 'first line'
    text = nmod.find_first_line(filepath, string)
    expect = 'Actual first line.'

    assert text == expect


def test_modify_file(rmnew):
    """Test modify_file function."""
    original = os.path.join(fixtures_dir, 'nmod.inp')
    new = os.path.join(fixtures_dir, 'nmod.new')
    expect_file = os.path.join(fixtures_dir, 'nmod.expect')
    reps = {
        'kkrtools_NKTAB': '250',
        'kkrtools_NE': '30',
    }

    nmod.modify_file(original, new, reps)

    with open(new, 'r') as f:
        output = f.readlines()

    with open(expect_file, 'r') as f:
        expect = f.readlines()

    assert output == expect
