from __future__ import absolute_import

from commands import getoutput
from subprocess import check_call

def get_current_branch_name():
    output = getoutput('git symbolic-ref HEAD')
    assert output.startswith('refs/heads/')
    return output[len('refs/heads/'):]


def merge_with_master(branch):
    check_call('git checkout master', shell=True)
    check_call('git pull upstream master', shell=True)
    check_call('git checkout %s' % branch, shell=True)
    check_call('git merge master', shell=True)



