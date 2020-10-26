from tkinter import BOTH, BOTTOM, NONE, RIGHT, END, Frame, Scrollbar, Tk, X, Y

from pyedit.lines import CustomText, TextLineNumbers
from pyedit.syntax_highlighting import Syntax
from pyedit.toolbar import Toolbar


class TextEditor(Frame):
    def __init__(self, master, filename) -> None:
        super().__init__(master)

        self.master = master
        self.filename = filename
        self.line_numbers = TextLineNumbers(self, width=20)
        self.syntax = Syntax(master)
        self.add_scrollbar()
        if filename is not None:
            self.open_file()

        bar = Toolbar(master, self.text)
        bar.current_file = filename
        bar.open_file_button()
        bar.save_file_button()
        bar.save_file_as_button()
        bar.post_to_hastebin_button()
        bar.run_button()
        bar.close_editor_button()
        bar.undo_button()
        bar.redo_button()
        bar.cut_button()
        bar.copy_button()
        bar.paste_button()
        bar.find_and_replace_button()
        bar.select_all_button()
        bar.deselect_all_button()
        bar.keyword_highlighting_button()
        bar.builtin_highlighting_button()
        bar.number_highlighting_button()
        bar.comment_highlighting_button()
        bar.string_highlighting_button()
        bar.definition_highlighting_button()
        bar.stackoverflow_button()

    def add_scrollbar(self) -> None:
        self.y_scrollbar = Scrollbar(self.master)
        self.x_scrollbar = Scrollbar(self.master, orient="horizontal")
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        self.x_scrollbar.pack(side=BOTTOM, fill=X)
        self.line_numbers.pack(side="left", fill=Y)

        self.text = CustomText(
            self.master,
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set,
            highlightcolor="white",
            wrap=NONE,
            undo=True
        )

        self.text.pack(fill=BOTH, side=RIGHT, expand=True)

        self.text.bind("<<Change>>", self.on_change)
        self.text.bind("<Configure>", self.on_change)
        self.text.bind("<KeyRelease>", self.on_key_release)

        self.y_scrollbar.config(command=self.text.yview)
        self.x_scrollbar.config(command=self.text.xview)
        self.line_numbers.attach(self.text)

    def on_change(self, event) -> None:
        self.line_numbers.redraw()

    def on_key_release(self, event) -> None:
        self.syntax.highlight(self.text)

    def open_file(self) -> None:
        with open(self.filename) as f:
            lines = f.read()

        self.text.insert(END, lines)
        self.syntax.highlight(self.text)


def run(filename) -> None:
    root = Tk()
    root.title("PyEdit")
    syntax = Syntax(root)
    syntax.load_colors()
    old_colors = syntax.colors
    texteditor = TextEditor(root, filename)
    texteditor.pack(side="top", fill=BOTH, expand=True)
    root.mainloop()
    if old_colors != syntax.colors:
        syntax.save_colors()
