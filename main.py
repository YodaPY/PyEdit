from tkinter import (
    Tk,
    Scrollbar,
    Text,
    RIGHT,
    Y,
    BOTH,
    YES,
    Frame,
    NONE,
    BOTTOM,
    X
)
from lines import (
    TextLineNumbers,
    CustomText
)
from toolbar import Toolbar
from syntax_highlighting import Syntax

class TextEditor(Frame):
    def __init__(
        self,
        master=None
    ) -> None:
        super().__init__(master)

        self.master = master
        self.line_numbers = TextLineNumbers(
            self,
            width=20
        )
        self.syntax = Syntax(master)
        self.add_scrollbar()
        bar = Toolbar(master, self.text)
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
        self.text.bind("<KeyRelease>")

    def add_scrollbar(self) -> None:
        self.y_scrollbar = Scrollbar(self.master)
        self.x_scrollbar = Scrollbar(self.master, orient='horizontal')
        self.y_scrollbar.pack(
            side=RIGHT,
            fill=Y
        )
        self.x_scrollbar.pack(
            side=BOTTOM,
            fill=X
        )
        self.line_numbers.pack(side="left", fill=Y)

        self.text = CustomText(
            self.master,
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set,
            highlightcolor="white",
            tabs=28,
            wrap=NONE,
            undo=True,
            maxundo=1
        )

        self.text.pack(
            fill=BOTH,
            side=RIGHT,
            expand=True
        )

        self.text.bind("<<Change>>", self.on_change)
        self.text.bind("<Configure>", self.on_change)
        self.text.bind("<KeyRelease>", self.on_key_release)

        self.y_scrollbar.config(
            command=self.text.yview
        )
        self.x_scrollbar.config(
            command=self.text.xview
        )
        self.line_numbers.attach(self.text)

    def on_change(self, event) -> None:
        self.line_numbers.redraw()

    def on_key_release(self, event) -> None:
        self.syntax.highlight(self.text)

def run() -> None:
    root = Tk()
    root.title("PyEdit")
    texteditor = TextEditor(root)
    texteditor.pack(
        side="top",
        fill=BOTH,
        expand=True
    )
    syntax = Syntax(root)
    syntax.load_colors()
    root.mainloop()
    syntax.save_colors()

run()