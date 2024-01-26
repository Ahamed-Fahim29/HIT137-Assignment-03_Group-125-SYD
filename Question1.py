import tkinter as t_in

class Cal(t_in.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cal")
        self.geometry("325x250")
        self.result_var = t_in.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Entry widget for display
        entry = t_in.Entry(self, textvariable=self.result_var, font=('Helvetica', 20), bd=10, relief=t_in.SOLID, justify=t_in.RIGHT)
        entry.grid(row=0, column=0, columnspan=4)

        # Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            btn = CalButton(self, text, row, col)

    def calculate(self):
        try:
            result = eval(self.result_var.get())
            self.result_var.set(result)
        except Exception as e:
            self.result_var.set("Error")

# Custom Button class for the Cal
class CalButton(t_in.Button):
    def __init__(self, Cal, text, row, col):
        super().__init__(Cal, text=text, font=('Helvetica', 16), bd=5, relief=t_in.RAISED, command=lambda: self.button_click(Cal, text))
        self.grid(row=row, column=col, sticky="nsew")

    def button_click(self, Cal, text):
        if text == "=":
            Cal.calculate()
        elif text == "C":
            Cal.result_var.set("")
        else:
            current_text = Cal.result_var.get()
            Cal.result_var.set(current_text + text)

# Run the application
if __name__ == "__main__":
    app = Cal()
    app.mainloop()
