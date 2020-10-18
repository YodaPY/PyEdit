import keyword
import builtins
from tkinter import END
from tokenize import (
    tokenize,
    NUMBER,
    STRING,
    TokenError
)
from io import BytesIO

def highlight(text) -> None:
    keywords = keyword.kwlist
    d = {}
    for kw in keywords:
        d[kw] = "#8f19f7"

    for bi in dir(builtins):
        d[bi] = "#1936f7"

    for key, hex_value in d.items():
        text.tag_remove(key, 1.0, END)
        first = 1.0

        while True:
            first = text.search(
                rf"\m{key}\M",
                first,
                nocase=False,
                stopindex=END,
                regexp=True
            )

            if first is None or first == "":
                break
            
            first_splitted = first.split(".")
            if len(first_splitted) == 1:
                break

            last = f"{first_splitted[0]}.{int(first_splitted[1]) + len(key)}"

            text.tag_add(key, first, last)
            first = last
            
        text.tag_config(
            key,
            foreground=hex_value
        )

    g = tokenize(BytesIO(text.get(1.0, END).encode('utf-8')).readline)

    try:
        for token in g:
            if token.type == 3:
                text.tag_add(
                    "token.string",
                    f"{token.start[0]}.{token.start[1]}",
                    f"{token.end[0]}.{token.end[1]}"
                )

            if token.type == 2:
                text.tag_add(
                    "token.number",
                    f"{token.start[0]}.{token.start[1]}",
                    f"{token.end[0]}.{token.end[1]}"
                )

            if token.type == 60:
                text.tag_add(
                    "token.comment",
                    f"{token.start[0]}.{token.start[1]}",
                    f"{token.end[0]}.{token.end[1]}"
                )

    except TokenError:
        pass

    text.tag_config(
        "token.number",
        foreground="#84db32"
    )
    text.tag_config(
        "token.comment",
        foreground="#326601"
    )
    text.tag_config(
        "token.string",
        foreground="#c79202"
    )