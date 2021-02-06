from pathlib import Path

import pytest

from scripts.create_new_workspace import makedir_iterable_structure


def test_recur_mkdir_on_regular_structure(mock_config, tmpdir):
    test_structure = {
        'folder': ['sub1', 'sub2'],
        'folder2': ['2sub1', '2sub2']
    }
    base = Path(tmpdir)
    expected = [base / 'folder' / 'sub1',
                base / 'folder' / 'sub2',
                base / 'folder2' / '2sub1',
                base / 'folder2' / '2sub2',
                base / 'folder2',
                base / 'folder']


    makedir_iterable_structure(test_structure, tmpdir)

    new_dirs = list(Path(tmpdir).rglob('*'))

    for expect in expected:
        assert expect in new_dirs
        new_dirs.remove(expect)

    # folder1/folder2 should be left
    assert new_dirs == []


def test_recur_mkdir_with_single_subfolder(mock_config, tmpdir):
    test_structure = {
        'folder': 'subfolder',
        'folder2': ['2sub1', '2sub2']
    }
    base = Path(tmpdir)
    expected = [base / 'folder' / 'subfolder',
                base / 'folder2' / '2sub1',
                base / 'folder2' / '2sub2',
                base / 'folder2',
                base / 'folder'
                ]


    makedir_iterable_structure(test_structure, tmpdir)

    new_dirs = list(Path(tmpdir).rglob('*'))

    for expect in expected:
        assert expect in new_dirs
        new_dirs.remove(expect)

    assert new_dirs == []


def test_recur_mkdir_structure_is_list(mock_config, tmpdir):
    test_structure = ['folder1', 'folder2']

    base = Path(tmpdir)
    expected = [base / 'folder1',
                     base / 'folder2',]

    makedir_iterable_structure(test_structure, tmpdir)

    new_dirs = list(Path(tmpdir).rglob('*'))

    for expect in expected:
        assert expect in new_dirs
        new_dirs.remove(expect)

    assert new_dirs == []


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_recur_mkdir_with_no_subfolder(mock_config, tmpdir, subtests):
    test_structure = {
        'folder': '',
        'folder2': ['2sub1', '2sub2']
    }

    test_structure2 = {
        'folder': None,
        'folder2': ['2sub1', '2sub2']
    }

    test_structures = [test_structure, test_structure2]

    base = Path(tmpdir)
    base_expected = [base / 'folder',
                base / 'folder2',
                base / 'folder2' / '2sub1',
                base / 'folder2' / '2sub2']


    for i, test_structure in enumerate(test_structures):
        # Clear test dir manually because we are doing subtests
        for tmp in tmpdir.listdir():
            tmp.remove()

        with subtests.test("Testing different emtpy values do not create directories", i=i):
            makedir_iterable_structure(test_structure, tmpdir)

            new_dirs = list(Path(tmpdir).rglob('*'))
            expected = base_expected.copy()
            for expect in expected:
                assert expect in new_dirs
                new_dirs.remove(expect)

            assert new_dirs == []

@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_recur_mkdir_on_nested_structure(mock_config, tmpdir, subtests):
    test_structure = {
        'folder': [{'sub1': 'sub1_nested'},
                   'sub2'],

        'folder2': ['2sub1', '2sub2']
    }
    test_structure2 = {
        'folder': ['sub2',
                   {'sub1': 'sub1_nested'},],

        'folder2': ['2sub1', '2sub2']}

    test_structures = [test_structure, test_structure2]
    base = Path(tmpdir)

    base_expected = [base / 'folder' / 'sub1',
                base / 'folder' / 'sub2',
                base / 'folder' / 'sub1' / 'sub1_nested',
                base / 'folder2' / '2sub1',
                base / 'folder2' / '2sub2',
                base / 'folder2',
                base / 'folder']

    for i, test_structure in enumerate(test_structures):
        # Clear test dir manually because we are doing subtests
        for tmp in tmpdir.listdir():
            tmp.remove()

        with subtests.test("Testing creating nested subdirectories", i=i):
            makedir_iterable_structure(test_structure, tmpdir)

            new_dirs = list(Path(tmpdir).rglob('*'))
            expected = base_expected.copy()
            for expect in expected:
                assert expect in new_dirs
                new_dirs.remove(expect)

            assert new_dirs == []


def test_recur_mkdir_on_double_nested(mock_config, tmpdir):
    test_structure = {
        'folder': [{'sub1': 'sub1_nested'},
                   'sub2'],

        'folder2': ['2sub1', {'f2_sub': {'f2_sub3': 'deeply_nested'}}]
    }

    base = Path(tmpdir)
    base_expected = [base / 'folder' / 'sub1',
                base / 'folder' / 'sub2',
                base / 'folder' / 'sub1' / 'sub1_nested',
                base / 'folder2' / '2sub1',
                base / 'folder2' / 'f2_sub',
                base / 'folder2' / 'f2_sub' / 'f2_sub3',
                base / 'folder2' / 'f2_sub' / 'f2_sub3' / 'deeply_nested',
                base / 'folder2',
                base / 'folder']


    makedir_iterable_structure(test_structure, tmpdir)

    new_dirs = list(Path(tmpdir).rglob('*'))
    expected = base_expected.copy()
    for expect in expected:
        assert expect in new_dirs
        new_dirs.remove(expect)

    assert new_dirs == []