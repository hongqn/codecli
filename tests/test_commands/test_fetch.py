from mock import patch, Mock
import codecli.commands.fetch as M

def test_fetch_should_add_remote_and_fetch():
    args = Mock(username='testuser')
    with patch.object(M, 'getoutput') as mock_getoutput, \
            patch.object(M, 'check_call') as mock_check_call:
        mock_getoutput.return_value = """\
origin  http://code.dapps.douban.com/codecli.git (fetch)
origin  http://code.dapps.douban.com/codecli.git (push)
"""
        M.main(args)

    mock_check_call.assert_any_call(['git', 'remote', 'add', 'testuser',
                                     'http://code.dapps.douban.com/testuser/codecli.git'])
    mock_check_call.assert_any_call(['git', 'fetch', 'testuser'])
