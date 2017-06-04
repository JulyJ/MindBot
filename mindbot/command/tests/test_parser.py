from mindbot.command.remember.parser import parse_tags


def test_tags():
    assert parse_tags('test #tag') == ['#tag']
