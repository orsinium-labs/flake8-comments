import re
import tokenize
from typing import Iterable, Iterator, Set


REX_WORD = re.compile(r'[A-Za-z]+')
# https://stackoverflow.com/a/1176023/8704691
REX1 = re.compile(r'(.)([A-Z][a-z]+)')
REX2 = re.compile(r'([a-z0-9])([A-Z])')


def get_words(text: str) -> Set[str]:
    text = REX1.sub(r'\1 \2', text)
    text = REX2.sub(r'\1 \2', text).lower()
    text = text.replace('_', ' ')
    return set(text.split())


def get_redundant_comments(
    tokens: Iterable[tokenize.TokenInfo],
) -> Iterator[tokenize.TokenInfo]:
    comment = None
    multiline_comment = False
    code_words: Set[str] = set()
    for token in tokens:
        if token.type == tokenize.NL:
            continue

        # remember first comment, skip multiline comments
        if token.type == tokenize.COMMENT:
            if multiline_comment:
                continue
            if comment is None:
                comment = token
            else:
                comment = None
                multiline_comment = True
            continue

        # skip lines without a single-line comment before
        if comment is None:
            continue
        multiline_comment = False

        # if this is a token on the next line after the comment,
        # extract words from it
        if token.start[0] == comment.start[0] + 1:
            code_words.update(get_words(token.string))
            continue

        # if we already 2 lines after the comment,
        # check if words in the code has all words from the comment
        comment_words = set(REX_WORD.findall(comment.string))
        if comment_words and not comment_words - code_words:
            yield comment
        code_words = set()
        comment = None
