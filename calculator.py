import tkinter as tk
from tkinter import messagebox
import numpy as np
from sympy import symbols, diff
import math

def calculate_derivative(expression, var):
    x = symbols(var)
    derivative = diff(expression, x)
    return str(derivative)

def multiply_matrices(matrix1, matrix2):
    try:
        result = np.dot(matrix1, matrix2)
        return result
    except ValueError:
        return "Error: Matrices are not compatible for multiplication."

def calculate_square_root(number):
    return math.sqrt(number)

def calculate_cube_root(number):
    return number ** (1 / 3)

def evaluate_expression(expression):
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to cover half the screen (horizontally)
        self.root.geometry(f"{screen_width // 2}x{screen_height // 2}")
        
        # Adjust the expression entry to cover more space
        self.expression_entry = tk.Entry(root, width=50, borderwidth=5, font=('Arial', 18))
        self.expression_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky='nsew')
        
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('sqrt', 5, 0), ('cbrt', 5, 1), ('clear', 5, 2), ('matrix', 5, 3),
            ('derivative', 6, 0, 2), ('(', 6, 2), (')', 6, 3)
        ]

        for button_info in buttons:
            text, row, col = button_info[:3]
            colspan = button_info[3] if len(button_info) == 4 else 1
            button = tk.Button(self.root, text=text, padx=40, pady=20, font=('Arial', 14), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, columnspan=colspan, sticky='nsew')

        # Make the grid cells expand with the window
        for i in range(1, 7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == '=':
            self.calculate_result()
        elif char == 'clear':
            self.expression_entry.delete(0, tk.END)
        elif char == 'sqrt':
            try:
                number = float(self.expression_entry.get())
                result = calculate_square_root(number)
                self.expression_entry.delete(0, tk.END)
                self.expression_entry.insert(0, result)
            except ValueError:
                messagebox.showerror("Error", "Invalid input for square root.")
        elif char == 'cbrt':
            try:
                number = float(self.expression_entry.get())
                result = calculate_cube_root(number)
                self.expression_entry.delete(0, tk.END)
                self.expression_entry.insert(0, result)
            except ValueError:
                messagebox.showerror("Error", "Invalid input for cube root.")
        elif char == 'matrix':
            self.open_matrix_multiplication_window()
        elif char == 'derivative':
            self.open_derivative_window()
        else:
            self.expression_entry.insert(tk.END, char)

    def calculate_result(self):
        expression = self.expression_entry.get()
        result = evaluate_expression(expression)
        self.expression_entry.delete(0, tk.END)
        self.expression_entry.insert(0, result)

    def open_matrix_multiplication_window(self):
        matrix_window = tk.Toplevel(self.root)
        matrix_window.title("Matrix Multiplication")
        tk.Label(matrix_window, text="Matrix 1 (comma-separated rows):").grid(row=0, column=0)
        matrix1_entry = tk.Entry(matrix_window, width=40)
        matrix1_entry.grid(row=0, column=1)
        tk.Label(matrix_window, text="Matrix 2 (comma-separated rows):").grid(row=1, column=0)
        matrix2_entry = tk.Entry(matrix_window, width=40)
        matrix2_entry.grid(row=1, column=1)

        def multiply():
            try:
                matrix1 = np.array(eval(matrix1_entry.get()))
                matrix2 = np.array(eval(matrix2_entry.get()))
                result = multiply_matrices(matrix1, matrix2)
                messagebox.showinfo("Matrix Multiplication Result", str(result))
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        multiply_button = tk.Button(matrix_window, text="Multiply", command=multiply)
        multiply_button.grid(row=2, column=0, columnspan=2)

    def open_derivative_window(self):
        derivative_window = tk.Toplevel(self.root)
        derivative_window.title("Calculate Derivative")
        tk.Label(derivative_window, text="Expression (e.g., x**2 + 3*x):").grid(row=0, column=0)
        expression_entry = tk.Entry(derivative_window, width=40)
        expression_entry.grid(row=0, column=1)
        tk.Label(derivative_window, text="Variable (e.g., x):").grid(row=1, column=0)
        variable_entry = tk.Entry(derivative_window, width=10)
        variable_entry.grid(row=1, column=1)

        def calculate():
            expression = expression_entry.get()
            variable = variable_entry.get()
            try:
                result = calculate_derivative(expression, variable)
                messagebox.showinfo("Derivative Result", result)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        calculate_button = tk.Button(derivative_window, text="Calculate", command=calculate)
        calculate_button.grid(row=2, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
