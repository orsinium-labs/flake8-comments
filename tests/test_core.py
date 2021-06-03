import tokenize

import pytest

from flake8_comments._core import get_redundant_comments


@pytest.mark.parametrize('comment, code_line, expected', [
    ('# hello world', 'hello = world', True),
    ('# hello world', 'hello = world()', True),
    ('# hello world example', '(hello, world) = example()', True),
    ('# hello world', 'class HelloWorld: pass', True),
    ('# hello world', 'class HelloWorldExample: pass', True),
    ('# hello world', 'def hello_world(): pass', True),
    ('# hello world', 'def hello_world_example(): pass', True),
    ('# hello world', 'hello_world = something()', True),
    ('# hello world', 'hello_world_example = something()', True),
    ('# oh hi mark', 'oh = "hi mark"', True),

    ('# create user', 'create_user()', True),
    ('# create a user', 'create_user()', True),
    ('# create the user', 'create_user()', True),
    ('# create user', 'create_user(force=True)', True),
    ('# init data storage', 'DataStorage.init()', True),

    ('# this is hello world example', 'hello = world', False),
    ('# hello world', 'something = else', False),
    ('# an example of\n# hello world', 'hello = world', False),
    ('# a multiline\n# example of\n# hello world', 'hello = world', False),
    ('# hello world', 'something = else\nhello = world', False),
])
def test_get_redundant_comments(comment: str, code_line: str, expected: bool):
    lines = comment.splitlines() + code_line.splitlines()
    readline = iter(lines).__next__
    tokens = tokenize.generate_tokens(readline)
    result = list(get_redundant_comments(tokens))
    assert len(result) == int(expected)
