import re
import textwrap
from typing import Iterator
from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    type: str
    value: str
    indent: int
    line_num: int

def lex_yidl(source_code: str) -> Iterator[Token]:
    """
    Indentation-aware line scanner for YIDL.
    Uses '%%' to mark the start of a raw Python block.
    Supports '#' for full-line and inline comments in the structural DSL.
    """
    lines = source_code.splitlines()
    idx = 0

    while idx < len(lines):
        original_line = lines[idx]

        line_no_comment = original_line.split('#', 1)[0]
        stripped = line_no_comment.strip()

        if not stripped:
            idx += 1
            continue

        indent = len(line_no_comment) - len(line_no_comment.lstrip())
        line_num = idx + 1

        if '%%' in stripped:
            prefix, inline_code = original_line.split('%%', 1)

            prefix_stripped = prefix.strip()
            if prefix_stripped:
                yield Token("STATEMENT", prefix_stripped, indent, line_num)

            code_block = []

            inline_stripped = inline_code.strip()
            if inline_stripped:
                code_block.append(inline_stripped)

            idx += 1

            while idx < len(lines):
                next_line = lines[idx]

                next_no_comment = next_line.split('#', 1)[0]
                next_stripped = next_no_comment.strip()

                if next_stripped:
                    next_indent = len(next_no_comment) - len(next_no_comment.lstrip())
                    if next_indent <= indent:
                        break

                code_block.append(next_line)
                idx += 1

            raw_python_code = textwrap.dedent('\n'.join(code_block)).strip()

            if raw_python_code:
                snippet_line_num = line_num if inline_stripped else line_num + 1
                yield Token("CODE_SNIPPET", raw_python_code, indent + 4, snippet_line_num)

            continue

        yield Token("STATEMENT", stripped, indent, line_num)
        idx += 1

if __name__ == "__main__":
    sample_yidl = """
    behavior Working:
        store = WorkingStore

        get: %%
            if not store.has():
                store.write(thaw(fallback.read()))
            return store.read()

        set(val, old_val): %%
            store.write(val)
            txm.mark_dirty(tx_group)

    behavior Commit:
        store = PublishedStore
        get: %% store.read()
    """

    print("--- LEXER OUTPUT ---")
    for token in lex_yidl(sample_yidl):
        print(token)
