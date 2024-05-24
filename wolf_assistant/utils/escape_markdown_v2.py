"""This script provides the `escape_markdown_v2` function, that helps to escape GPT-generated markdown before sending
it through Telegram Bot API using parse_mode='MarkdownV2'. Official Telegram Bot API documentation
(https://core.telegram.org/bots/api#markdownv2-style) states:

Inside pre and code entities, all '`' and '\' characters must be escaped with a preceding '\' character.
In all other places characters '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}',
'.', '!' must be escaped with the preceding character '\'.

Not implemented yet:
Inside the (...) part of the inline link and custom emoji definition, all ')' and '\' must be escaped with
a preceding '\' character.
"""

import re
from typing import Generator


SPECIAL_CHAR_REGEX = re.compile(r'([\\_*[\]()~`>#+\-=|{}.!])')
BIG_CODE_BLOCK_REGEX = re.compile(r'(?is)(?<!`)(```\w* *\n)(.*?)(\n```)(?!`)')
SMALL_CODE_BLOCK_REGEX = re.compile(r'(?<!`)`[^\n`]*?`(?!`)')
MARKDOWN_V2_GPT_PROMPT = """Make sure to ALWAYS format your code using backticks:
```[lang]
[code block]
```
or `inline code`. Don't use bold, italic, underline or strikethrough text.
"""


def escape_all_special_chars(s: str) -> str:
    return SPECIAL_CHAR_REGEX.sub(r'\\\1', s)


def merge_nested_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merges integer intervals which are entirely contained within other intervals."""
    if not intervals:
        return []
    res = []
    for interval in sorted(intervals, key=lambda t: (t[0], -t[1])):
        if res and res[-1][0] <= interval[0] <= interval[1] <= res[-1][1]:
            pass  # skip interval if its fully contained in a previous interval
        else:
            res.append(interval)
    return res


def escape_code_block(s: str) -> str:
    assert len(s) >= 2, s
    big_match = BIG_CODE_BLOCK_REGEX.fullmatch(s)
    if big_match:
        start, code, end = big_match.groups()
        code = code.replace('\\', '\\\\').replace('`', '\\`')
        return f'{start}{code}{end}'
    else:
        # assume s is a small code block: "`example`"
        # SMALL_CODE_BLOCK_REGEX guarantees that only part[0] == part[-1] == '`'
        # so we only need to escape the '\' character
        return s.replace('\\', '\\\\')


def escape_markdown_v2(s: str) -> str:
    def iter_over_outside_inside_code_blocks(s: str) -> Generator[tuple[str, str], None, None]:
        code_intervals = [m.span() for reg in (BIG_CODE_BLOCK_REGEX, SMALL_CODE_BLOCK_REGEX) for m in reg.finditer(s)]
        code_intervals = merge_nested_intervals(code_intervals)
        prev_code_end = 0
        for code_start, code_end in code_intervals:
            if prev_code_end < code_start:
                yield 'outside', s[prev_code_end: code_start]
            yield 'inside', s[code_start: code_end]
            prev_code_end = code_end
        if code_intervals and code_intervals[-1][1] < len(s):
            yield 'outside', s[code_intervals[-1][1]:]
        if not code_intervals:
            yield 'outside', s

    return ''.join(
        escape_all_special_chars(s)
        if where == 'outside'
        else escape_code_block(s)
        for where, s in iter_over_outside_inside_code_blocks(s)
    )


if __name__ == '__main__':
    example_string = """
0.
1. one > ~ < &

```python
s = "`` hi !"
with \\x00 \\n escaped sequences!
`and more backticks!`
```

some text. `some inline code with \\x00 \\n escaped sequences!`.
end.
[links](are ruined for now) :(
    """.strip()
    print(escape_markdown_v2(example_string))
