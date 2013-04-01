from subprocess import check_call
from nose.tools import eq_
import codecli.utils as M
from tests.utils import mkdtemp


def test_get_branches_should_return_a_list_of_branch_names():
    with mkdtemp(cd=True):
        check_call(['git', 'init'])
        open('test', 'w').close()
        check_call(['git', 'add', 'test'])
        check_call(['git', 'commit', '-m', 'test'])

        branches = M.get_branches()
    eq_(branches, ['master'])
