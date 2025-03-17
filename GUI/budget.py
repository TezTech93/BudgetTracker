import csv
import datetime as dt
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

# Constants
DAILY = dt.timedelta(days=1)
WEEKLY = dt.timedelta(weeks=1)
BI_WEEKLY = dt.timedelta(weeks=2)
MONTHLY = dt.timedelta(days=30)
YEARLY = dt.timedelta(days=365)

WEEKDAYS = {
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
    3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'
}

# Classes
class Budget:
    def __init__(self, incomes=None, expenses=None, schedule=None):
        self.incomes = incomes if incomes else []
        self.expenses = expenses if expenses else []
        self.schedule = schedule if schedule else []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def add_income(self, income):
        self.incomes.append(income)

    def save_to_csv(self, filename="budget.csv"):
        """Saves incomes and expenses to a CSV file."""
        file_exists = Path(filename).exists()
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                # Write header if file doesn't exist
                writer.writerow(["Type", "Name", "Amount", "Date", "Occurrence"])

            # Write incomes
            for income in self.incomes:
                writer.writerow(["Income", income.source, income.amt, income.date, income.occurrence])

            # Write expenses
            for expense in self.expenses:
                writer.writerow(["Expense", expense.name, expense.amt, expense.due_date, expense.occurrence])

        messagebox.showinfo("Success", f"Data saved to {filename}")


class Expense:
    def __init__(self, name, amount, due_date, occurrence):
        self.name = name
        self.amt = amount
        self.due_date = due_date
        self.occurrence = occurrence


class Income:
    def __init__(self, source, amount, date, occurrence):
        self.source = source
        self.amt = amount
        self.date = date
        self.occurrence = occurrence


# GUI Application
class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.budget = Budget()

        # Make the window resizable
        self.root.geometry("600x400")  # Initial size
        self.root.minsize(400, 300)  # Minimum size
        self.root.maxsize(1200, 800)  # Maximum size

        # Configure grid weights for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(5, weight=1)

        # Type
        tk.Label(root, text="Type (Income/Expense):", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.type_var = tk.StringVar(value="Income")
        type_menu = ttk.Combobox(root, textvariable=self.type_var, values=["Income", "Expense"], state="readonly")
        type_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Name
        tk.Label(root, text="Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(root, font=("Arial", 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Amount
        tk.Label(root, text="Amount:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = tk.Entry(root, font=("Arial", 12))
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Date
        tk.Label(root, text="Date (e.g., 1 for 1st, or 'today'):", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = tk.Entry(root, font=("Arial", 12))
        self.date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Occurrence
        tk.Label(root, text="Occurrence:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.occurrence_var = tk.StringVar(value="WEEKLY")
        occurrence_menu = ttk.Combobox(root, textvariable=self.occurrence_var, values=["DAILY", "WEEKLY", "BI_WEEKLY", "MONTHLY", "YEARLY"], state="readonly")
        occurrence_menu.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Add Button
        tk.Button(root, text="Add", command=self.add_item, font=("Arial", 12)).grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Save Button
        tk.Button(root, text="Save to CSV", command=self.save_to_csv, font=("Arial", 12)).grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def add_item(self):
        """Adds an income or expense based on user input."""
        type_ = self.type_var.get().lower()
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        occurrence = self.occurrence_var.get()

        # Validate amount
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        # Validate date
        if date.lower() == "today":
            date = dt.datetime.now().day
        else:
            try:
                date = int(date)
            except ValueError:
                messagebox.showerror("Error", "Date must be a number or 'today'.")
                return

        # Add item to budget
        if type_ == "income":
            self.budget.add_income(Income(name, amount, date, globals()[occurrence]))
        elif type_ == "expense":
            self.budget.add_expense(Expense(name, amount, date, globals()[occurrence]))

        messagebox.showinfo("Success", f"{type_.capitalize()} added successfully!")

    def save_to_csv(self):
        """Saves the budget data to a CSV file."""
        self.budget.save_to_csv()


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
