import tkinter as t_in
import math

class Cal(t_in.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cal")
        self.geometry("325x297")
        self._var = t_in.StringVar() #private variable for incapsulation
        self.create_widgets()

    def create_widgets(self):
        # display
        entry = t_in.Entry(self, textvariable=self._var, font=('Arial', 20), bd=12, relief=t_in.SOLID, justify=t_in.RIGHT)
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Buttons
        buttons = [
            ('√', 1, 0), ('x²', 1, 1), ('log', 1, 2), ('ln', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('C', 5, 1), ('=', 5, 2), ('+', 5, 3)
        ]

        for (text, row, col) in buttons:
            btn = CalButton(self, text, row, col)

    @property
    def var(self):
        return self._var.get()

    @var.setter
    def var(self, value):
        self._var.set(value)

    def calculate(self):
        try:
            result = eval(self.var)
            self.var = str(result)
        except Exception as e:
            self.var = "Error"

    def square_root(self):
        try:
            value = float(self.var)
            result = math.sqrt(value)
            self.var = str(result)
        except Exception as e:
            self.var = "Error"

    def square(self):
        try:
            value = float(self.var)
            result = value ** 2
            self.var = str(result)
        except Exception as e:
            self.var = "Error"

    def logarithm(self):
        try:
            value = float(self.var)
            result = math.log10(value)
            self.var = str(result)
        except Exception as e:
            self.var = "Error"

    def natural_logarithm(self):
        try:
            value = float(self.var)
            result = math.log(value)
            self.var = str(result)
        except Exception as e:
            self.var = "Error"

class CalButton(t_in.Button):
    def __init__(self, cal, text, row, col):
        super().__init__(cal, text=text, font=('Arial', 16), bd=5, relief=t_in.RAISED, command=lambda: self.button_click(cal, text))
        self.grid(row=row, column=col, sticky="nsew")

    def button_click(self, cal, text):
        
        if text == "√":
            cal.square_root()
        elif text == "x²":
            cal.square()
        elif text == "log":
            cal.logarithm()
        elif text == "ln":
            cal.natural_logarithm()
        elif text == "=":
            cal.calculate()
        elif text == "C":
            cal.var = ""
        else:
            current_text = cal.var
            cal.var = current_text + text

if __name__ == "__main__":
    app = Cal()
    app.mainloop()