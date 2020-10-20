import keyword
import builtins
import os
from tkinter import END
from tokenize import (
    tokenize,
    NUMBER,
    STRING,
    TokenError
)
from io import BytesIO
from re import match
from json import load, dump

class Syntax:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if Syntax._instance is None:
            Syntax._instance = _Syntax(*args, **kwargs)
        return Syntax._instance

    def __getattr__(self, name):
        return getattr(Syntax._instance, name)

    def __setattr__(self, name, value):
        return setattr(Syntax._instance, name, value)

class _Syntax:
    def __init__(
        self,
        master
    ) -> None:

        self.master = master
        self.colors = {}

    def load_colors(self):
        with open("syntax_colors.json") as f:
            data = load(f)

        self.colors.update(**data)

    def save_colors(self):
        with open("syntax_colors.json", "w") as f:
            dump(self.colors, f)

    def highlight(self, text) -> None:
        keywords = keyword.kwlist
        d = {}

        for kw in keywords:
            d[kw] = self.colors["keyword"] ##8f19f7

        for bi in dir(builtins):
            d[bi] = self.colors["builtin"] ##1936f7

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

                if token.type == 1:
                    if match(rf"def\s+{token.string}", token.line):
                        text.tag_add(
                            "token.definition",
                            f"{token.start[0]}.{token.start[1]}",
                            f"{token.end[0]}.{token.end[1]}"
                        )

        except TokenError:
            pass

        text.tag_config(
            "token.number",
            foreground=self.colors["number"] ##56a30a
        )
        text.tag_config(
            "token.comment",
            foreground=self.colors["comment"] ##979399
        )
        text.tag_config(
            "token.string",
            foreground=self.colors["string"] ##326601
        )
        text.tag_config(
            "token.definition",
            foreground=self.colors["definition"] ##e39a24
        )