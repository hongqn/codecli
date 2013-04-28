from subprocess import check_call
from nose.tools import eq_
from mock import patch
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


def test_get_remote_repo_url_should_work():
    with patch.object(M, 'getoutput') as mock_getoutput:
        mock_getoutput.return_value = """\
origin  http://code.dapps.douban.com/testrepo.git (fetch)
origin  http://code.dapps.douban.com/testrepo.git (push)
upstream    http://code.dapps.douban.com/testrepo.git (fetch)
upstream    http://code.dapps.douban.com/testrepo.git (push)
"""

        repourl = M.get_remote_repo_url('origin')
    eq_(repourl, 'http://code.dapps.douban.com/testrepo')
 
