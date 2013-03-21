from mock import patch, Mock
from nose.tools import eq_
import codecli.commands.pullreq as M

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
    
