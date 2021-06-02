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

    ('# this is hello world example', 'hello = world', False),
])
def test_get_redundant_comments(comment, code_line, expected):
    readline = iter((comment, code_line)).__next__
    tokens = tokenize.generate_tokens(readline)
    result = list(get_redundant_comments(tokens))
    assert len(result) == int(expected)
