import os
from contextlib import contextmanager
import tempfile
import shutil

@contextmanager
def mkdtemp(cd=False):
    dir = tempfile.mkdtemp()
    try:
        if cd:
            with chdir(dir):
                yield dir
        else:
            yield dir
    finally:
        shutil.rmtree(dir)


@contextmanager
def chdir(dir):
    cwd = os.getcwd()
    os.chdir(dir)
    try:
        yield dir
    finally:
        os.chdir(cwd)
