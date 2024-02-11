import tkinter as tk
import math

class BasicCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x500")  # Adjust size
        self.result_var = tk.StringVar()  # Stores the current expression
        self.create_widgets()

    def create_widgets(self):
        # Display field
        display = tk.Entry(self, textvariable=self.result_var, font=('Arial', 24), bd=10, relief=tk.SOLID, justify=tk.RIGHT)
        display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Buttons configuration
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('√', 5, 0), ('x²', 5, 1), ('log', 5, 2), ('ln', 5, 3)
        ]

        for (text, row, col) in buttons:
            button_action = lambda x=text: self.calculate(x)
            tk.Button(self, text=text, font=('Arial', 20), command=button_action).grid(row=row, column=col, sticky="nsew")

        # Adjust button grid size
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)

    def calculate(self, value):
        if value == 'C':
            self.result_var.set('')
        elif value == '=':
            try:
                # Calculate the expression and update display
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except Exception as e:
                self.result_var.set("Error")
        elif value in ('√', 'x²', 'log', 'ln'):
            self.perform_special_operation(value)
        else:
            # Modify value to the current expression
            current = self.result_var.get()
            self.result_var.set(current + value)

    def perform_special_operation(self, operation):
        try:
            current_value = float(self.result_var.get())
            if operation == '√':
                result = math.sqrt(current_value)
            elif operation == 'x²':
                result = current_value ** 2
            elif operation == 'log':
                result = math.log10(current_value)
            elif operation == 'ln':
                result = math.log(current_value)
            self.result_var.set(str(result))
        except Exception as e:
            self.result_var.set("Error")

if __name__ == "__main__":
    app = BasicCalculator()
    app.mainloop()