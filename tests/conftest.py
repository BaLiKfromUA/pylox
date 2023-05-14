import sys
import os
from distutils.dir_util import copy_tree

import pytest


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # copy test data to tmpdir
    copy_tree(
        str(os.path.dirname(os.path.realpath(__file__))) + "/data", str(tmpdir)
    )
    # chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield
