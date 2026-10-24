import textwrap


def render_box(title: str, lines = (), width: int = 76) -> str:
    content = [title, ""]

    for line in lines:
        paragraphs = str(line).splitlines()

        if not paragraphs:
            paragraphs = [""]

        for paragraph in paragraphs:
            wrapped_lines = textwrap.wrap(paragraph, width = width, break_long_words = True)

            if not wrapped_lines:
                wrapped_lines = [""]

            content.extend(wrapped_lines)

    rows = [" " + "_" * (width + 2) + " "]

    for line in content:
        row = "| " + line.ljust(width) + " |"

        rows.append(row)

    rows.append("|" + "_" * (width + 2) + "|")

    return "\n".join(rows)


def show_box(title: str, lines = ()) -> None:
    box = render_box(title, lines)

    print(box)


def describe_options(options) -> list[str]:
    descriptions = []

    for option in options:
        description = option.describe()

        descriptions.append(description)

    return descriptions
