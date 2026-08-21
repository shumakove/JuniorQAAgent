from agent.tools import get_git_diff

def test_get_git_diff():
    diff = get_git_diff()

    assert isinstance(diff, str)
    