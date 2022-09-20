import tkinter as tk

LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"
LIGHT_BLUE = "#CCEDFF"

SMALL_FONT_STYLE = ('Arial', 12)
LARGE_FONT_STYLE = ('Arial', 30, 'bold')
DIGIT_FONT_STYLE = ('Arial', 18, 'bold')
DEFAULT_FONT_STYLE = ('Arial', 18)


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        # "#e8f7ff , #e0f4ff"
        self['bg'] = "#e8f7ff"

    def on_leave(self, e):
        self['bg'] = self.defaultBackground


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('325x505')
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expressions = ""
        self.current_expressions = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_label()

        self.digits = {
            7: (2, 1), 8: (2, 2), 9: (2, 3),
            4: (3, 1), 5: (3, 2), 6: (3, 3),
            1: (4, 1), 2: (4, 2), 3: (4, 3),
            ".": (5, 3),  0: (5, 2),
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluvate())
        self.window.bind("%", lambda event: self.percentage())
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        self.window.bind("<Escape>", lambda event: self.clear())
        self.window.bind("<Delete>", lambda event: self.ce())
        self.window.bind("q", lambda event: self.square())
        self.window.bind("r", lambda event: self.reciprocal())
        self.window.bind("@", lambda event: self.sqrt())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_ce_button()
        self.create_backspace_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_reciprocal_button()
        self.create_percentage_button()
        self.create_plus_minus_button()

    def create_display_label(self):
        total_label = tk.Label(self.display_frame, text=self.total_expressions, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expressions, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill='both')
        return frame

    def add_to_expression(self, value):
        self.current_expressions += str(value)
        self.update_label()

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = HoverButton(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGIT_FONT_STYLE, borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def plus_minus(self):
        try:
            self.current_expressions = str(eval(f"{self.current_expressions}*-1"))
        except Exception as e:
            self.current_expressions = ""
        finally:
            self.update_label()

    def create_plus_minus_button(self):
        button = HoverButton(self.buttons_frame, text="\u00B1", bg=WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.plus_minus)
        button.grid(row=5, column=1, sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expressions += operator
        self.total_expressions += self.current_expressions
        self.current_expressions = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 1
        for operator, symbol in self.operations.items():
            button = HoverButton(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def percentage(self):
        try:
            expression = self.total_expressions
            tot = float(expression[:-1])
            operator = expression[-1:]
            percent = float(eval(f"{self.current_expressions}*0.01"))
            if operator == '*' or operator == '/':
                self.current_expressions = str(percent)
            else:
                self.current_expressions = str("{:.2f}".format(percent * tot))
        except Exception as e:
            self.current_expressions = ""
        finally:
            self.update_label()

    def create_percentage_button(self):
        button = HoverButton(self.buttons_frame, text="\u0025", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.percentage)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def ce(self):
        self.current_expressions = ""
        self.update_label()

    def create_ce_button(self):
        button = HoverButton(self.buttons_frame, text="CE", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.ce)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def clear(self):
        self.current_expressions = ""
        self.total_expressions = ""
        self.update_total_label()
        self.update_label()

    def create_clear_button(self):
        button = HoverButton(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR,
                        font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def backspace(self):
        self.current_expressions = self.current_expressions[:-1]
        self.update_label()

    def create_backspace_button(self):
        button = HoverButton(self.buttons_frame, text="\u2190", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.backspace)
        button.grid(row=0, column=4, sticky=tk.NSEW)

    def reciprocal(self):
        try:
            expression = self.current_expressions
            self.current_expressions = str(eval(f"{self.current_expressions}**-1"))
            if self.total_expressions == "":
                self.total_expressions = "1/(" + expression + ")"
                self.update_total_label()
        except Exception as e:
            self.current_expressions = ""
        finally:
            self.update_label()

    def create_reciprocal_button(self):
        button = HoverButton(self.buttons_frame, text="\u215Fx", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.reciprocal)
        button.grid(row=1, column=1, sticky=tk.NSEW)

    def square(self):
        try:
            expression = self.current_expressions
            self.current_expressions = str(eval(f"{self.current_expressions}**2"))
            if self.total_expressions == "":
                self.total_expressions = "sqr(" + expression + ")"
                self.update_total_label()
        except Exception as e:
            self.current_expressions = ""
        finally:
            self.update_label()

    def create_square_button(self):
        button = HoverButton(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=1, column=2, sticky=tk.NSEW)

    def sqrt(self):
        try:
            expression = self.current_expressions
            self.current_expressions = str(eval(f"{self.current_expressions}**0.5"))
            if self.total_expressions == "":
                self.total_expressions = "\u221a(" + expression + ")"
                self.update_total_label()
        except Exception as e:
            self.current_expressions = ""
        finally:
            self.update_label()

    def create_sqrt_button(self):
        button = HoverButton(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=1, column=3, sticky=tk.NSEW)

    def evaluvate(self):
        self.total_expressions += self.current_expressions
        self.update_total_label()

        try:
            self.current_expressions = str(eval(self.total_expressions))
            self.total_expressions = ""
        except Exception as e:
            self.current_expressions = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = HoverButton(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluvate)
        button.grid(row=5, column=4, sticky=tk.NSEW)

    def update_total_label(self):
        expression = self.total_expressions[:30]
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f"{symbol}")
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expressions[:13])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()