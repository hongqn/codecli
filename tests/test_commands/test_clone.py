from mock import patch, Mock
import codecli.commands.clone as M


def test_should_run_git_clone():
    args = Mock(repo='repo', dir=None)
    with patch.object(M, 'check_call') as mock_check_call, \
            patch.object(M, 'cd') as mock_cd:
        M.main(args)

    mock_cd.assert_called_with('repo')
    mock_check_call.assert_any_call(['git', 'clone',
                                     'http://code.dapps.douban.com/repo.git'])


def test_should_run_git_clone_with_dir_when_dir_is_given():
    args = Mock(repo='repo', dir='.')
    with patch.object(M, 'check_call') as mock_check_call, \
            patch.object(M, 'cd') as mock_cd:
        M.main(args)

    mock_cd.assert_called_with('.')
    mock_check_call.assert_any_call(['git', 'clone',
                                     'http://code.dapps.douban.com/repo.git',
                                     '.'])
