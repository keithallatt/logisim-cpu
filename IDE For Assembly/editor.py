"""

EDITOR.PY

"""

from tkinter import *
from tkinter import filedialog
import re
import os

from os.path import expanduser

import simulated_cpu

import time


""" Temporary business, but until the codes get done through plist"""

CPU_COMMAND_CODES = {
    "SET_MEM": "0",
    "LOAD_A": "1",
    "LOAD_B": "2",
    "WRITE_A": "3",
    "WRITE_B": "4",
    "ADD_A_B": "5",
    "SUB_A_B": "6",
    "SET_A": "7",
    "SET_B": "8",
    "NC_JUMP": "9",
    "C_JUMP": "a",
    "MUL_A_B": "b",
    "DIV_A_B": "c",
    "MOD_IR": "d",
    "LS_REG": "e",
    "HALT": "f"
}

regex = re.compile("("+"|".join(CPU_COMMAND_CODES.keys())+")\s+([0-9]|[a-f])")

current_working_file = None

# don't copy paste! write in explicitly.
current_assembly_compiler = os.getenv("HOME")+"/Documents/LogisimCPU/" \
                            "Compiler/V1/AssemblyCompilerV1.py"
# print(os.path.exists(current_assembly_compiler))


def os_script(x, y):
    return "python3 "+x+" "+y


class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.text_widget = None

    def attach(self, text_widget):
        self.text_widget = text_widget

    def redraw(self):
        # redraw line numbers
        self.delete("all")

        i = self.text_widget.index("@0,0")
        num_lines = 0
        while True:
            next_i = self.text_widget.index("%s+1line" % i)

            line_content = self.text_widget.get(i, next_i)

            dline = self.text_widget.dlineinfo(i)

            if dline is None:
                break

            if line_content.strip() != "":
                num_lines += 1

            y = dline[1]

            linenum = hex(num_lines)[2:]

            if not regex.match(line_content.strip()):
                linenum = "ERR"
                try:
                    if line_content.strip()[0] == "#":  # comment, ignore
                        linenum = "CMT"
                except IndexError:
                    pass

                num_lines -= 1 # don't over count

            if line_content.strip() == "":
                linenum = ""
                num_lines += 1

            if len(linenum) == 1:
                linenum = "0"+linenum

            self.create_text(2, y, anchor="nw", text=linenum)
            i = next_i


class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.config(borderwidth=2, relief="groove")

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except TclError:
            # may mask other errors, but fixes
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
           args[0:3] == ("mark", "set", "insert") or
           args[0:2] == ("xview", "moveto") or
           args[0:2] == ("xview", "scroll") or
           args[0:2] == ("yview", "moveto") or
           args[0:2] == ("yview", "scroll")):
                self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class Editor(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        #Frame.geometry("700x700")  # controls size


        self.font = ("Courier New", 14)  # can later change with plist

        self.text = CustomText(self)
        self.text.config(font=self.font)
        self.vsb = Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        self.config(width=700, height=350)
        self.pack(side="top", fill="both", expand=False)

    def _on_change(self, event):
        self.linenumbers.redraw()


editor = None


def get_editor_content() -> str:
    if editor is None:
        raise Exception("Editor Does Not Exist")
    return editor.text.get("1.0", END)


def set_editor_content(content: str):
    if editor is None:
        raise Exception("Editor Does Not Exist")
    editor.text.delete(1.0, END)
    editor.text.insert(END, content)


def save_file():
    global current_working_file
    home = expanduser("~")

    if current_working_file is None:
        f = filedialog.asksaveasfilename(initialdir=home, title="Select file")

        # asksaveasfile return `None`  if dialog closed with "cancel".
        if f is None or f == '':
            return

        current_working_file = f

        f = open(f, 'w')

        text2save = str(get_editor_content())  # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()
    else:
        f = open(str(current_working_file), 'w')
        f.write(get_editor_content())
        f.close()


def open_file():
    global current_working_file
    home = expanduser("~")

    f = filedialog.askopenfilename(initialdir=home, title="Select file")

    contents = open(f, 'r').read()

    current_working_file = f
    set_editor_content(contents)

    pass


def compile_file():
    global current_working_file

    if current_working_file is None or current_working_file.strip() == "":
        save_file()

    try:
        cmd = os_script(current_assembly_compiler, current_working_file)
        print(cmd)
        os.system(cmd)
    except Exception:
        raise Exception("Compile Failed")


def run_file(outputLabel):
    global current_working_file

    compile_file()  # need to compile first

    compiled_file = current_working_file[0:current_working_file.rfind(".")]\
        + "_Compiled"

    content = open(compiled_file, 'r').read()

    content = content.replace("v2.0 raw\n", "")

    cpu = simulated_cpu.CPU()

    content = content.split()

    cpu.set_instructions(content)

    while cpu.is_enabled():
        cpu.fetch()
        cpu.decode()
        cpu.execute()

    outputLabel.config(text=str(cpu))
    outputLabel.update()


if __name__ == "__main__":
    root = Tk()
    editor = Editor(root)

    root.title("ASSEMBLY IDE")
    root.geometry("700x700")  # controls size

    output = Label(root)
    output.config(text="")
    output.pack()

    menubar = Menu(root)

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Compile", command=compile_file)
    filemenu.add_command(label="Run", command=lambda: run_file(output))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    #helpmenu = Menu(menubar, tearoff=0)
    #helpmenu.add_command(label="About", command=sample)
    #menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    root.config(menu=menubar)

    root.mainloop()
