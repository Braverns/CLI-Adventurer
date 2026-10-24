from __future__ import annotations
import textwrap

def render_box(title: str, lines=(), width: int = 76) -> str:
    content = [title, ""]
    for line in lines:
        for paragraph in str(line).splitlines() or [""]:
            content.extend(textwrap.wrap(paragraph, width=width, break_long_words=True) or [""])
    rows = [" " + "_" * (width + 2) + " "]
    rows.extend("| " + line.ljust(width) + " |" for line in content)
    rows.append("|" + "_" * (width + 2) + "|")
    return "\n".join(rows)

def show_box(title: str, lines=()) -> None:
    print(render_box(title, lines))

def describe_options(options) -> list[str]:
    # Duck typing: pilihan biasa dan pilihan cek memiliki describe().
    return [option.describe() for option in options]
