import tkinter as tk
from tkinter import ttk
import csv
import json
import re 

def totalAmount():
    total = 0

    with open("data.csv", mode='r') as data:
        dataReader = csv.DictReader(data)
        for row in dataReader:
            total += float(row["Amount"])

    return total

total_amount = totalAmount()

def update_total_label():
    global total_amount
    total_amount = totalAmount()
    total_label.config(text=f"Total Amount: £{total_amount:.2f}")

def open_receipt_window():
    global receipt_window
    receipt_window = tk.Toplevel(root)
    receipt_window.title("Enter Receipt")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    receipt_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    padding = 10

    date_label = tk.Label(receipt_window, text="Date (DD/MM/YY):")
    date_label.pack(pady=(padding, 0))

    global date_var
    date_var = tk.StringVar(receipt_window)
    date_entry = tk.Entry(receipt_window, textvariable=date_var)
    date_entry.pack(pady=(0, padding))

    amount_label = tk.Label(receipt_window, text="Amount in pounds:")
    amount_label.pack(pady=(padding, 0))
    amount_entry = tk.Entry(receipt_window)
    amount_entry.pack(pady=(0, padding))

    category_label = tk.Label(receipt_window, text="Category:")
    category_label.pack(pady=(padding, 0))

    global category_var
    category_var = tk.StringVar(receipt_window)
    category_var.set(category_options[0])
    category_dropdown = ttk.Combobox(receipt_window, textvariable=category_var, values=category_options, width=20)
    category_dropdown.pack(pady=(0, padding))

    button_enter = tk.Button(receipt_window, text="Enter Receipt", command=lambda: enter_receipt(date_entry.get(), amount_entry.get(), category_var.get()))
    button_enter.pack(pady=(padding, 0))

# Function to validate date
def validate_date(P):
    if P == "" or re.match(r"\d{2}/\d{2}/\d{2}$", P):
        return True
    else:
        return False

def enter_receipt(date, amount, category):
    infoGet(date, amount, category)
    receipt_window.destroy()
    update_total_label()

def infoGet(dt, amt, cat):
    columns = ["Date", "Amount", "Category"]
    dataList = {
        "Date": dt,
        "Amount": amt,
        "Category": cat
    }

    with open("data.csv", mode='a', newline='') as data:
        dataWriter = csv.DictWriter(data, fieldnames=columns)
        if data.tell() == 0:
            dataWriter.writeheader()
        dataWriter.writerow(dataList)

def close_program():
    root.destroy()

def show_category_popup():
    global category_popup
    category_popup = tk.Toplevel(root)
    category_popup.title("Select Category")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 200
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    category_popup.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    padding = 10

    category_label = tk.Label(category_popup, text="Select Category:")
    category_label.pack(pady=(padding, 0))

    global category_var_popup
    category_var_popup = tk.StringVar(category_popup)
    category_var_popup.set(category_options[0])
    category_dropdown_popup = ttk.Combobox(category_popup, textvariable=category_var_popup, values=category_options, width=20)
    category_dropdown_popup.pack(pady=(0, padding))

    button_calculate_category_total_popup = tk.Button(category_popup, text="Calculate Category Total", command=calculate_category_total_popup)
    button_calculate_category_total_popup.pack(pady=(padding, 0))

def calculate_category_total_popup():
    selected_category = category_var_popup.get()

    total = 0
    with open("data.csv", mode='r') as data:
        dataReader = csv.DictReader(data)
        for row in dataReader:
            if row["Category"] == selected_category:
                total += float(row["Amount"])

    category_total_label_popup.config(text=f"Total Amount for {selected_category}: £{total:.2f}")
    category_popup.destroy()

def open_add_category_window():
    global add_category_window
    add_category_window = tk.Toplevel(root)
    add_category_window.title("Add Category")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 150
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    add_category_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    padding = 10

    category_label = tk.Label(add_category_window, text="New Category:")
    category_label.pack(pady=(padding, 0))
    global new_category_entry
    new_category_entry = tk.Entry(add_category_window)
    new_category_entry.pack(pady=(0, padding))

    button_add_category = tk.Button(add_category_window, text="Add Category", command=add_category)
    button_add_category.pack(pady=(padding, 0))

def add_category():
    new_category = new_category_entry.get()

    # Load existing categories
    with open('categories.json', 'r') as file:
        category_data = json.load(file)
    existing_categories = category_data['categories']

    # Add the new category
    existing_categories.append(new_category)

    # Write back to the JSON file
    with open('categories.json', 'w') as file:
        json.dump({'categories': existing_categories}, file)

    # Update category_options
    category_options.append(new_category)

    add_category_window.destroy()

# Load categories from JSON file
with open('categories.json', 'r') as file:
    category_data = json.load(file)
category_options = category_data['categories']

root = tk.Tk()
root.title("Receipt Manager")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 500
window_height = 400
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

padding = 10

button_open_receipt = tk.Button(root, text="Enter a New Receipt", command=open_receipt_window)
button_open_receipt.pack(pady=(padding, 0))

total_label = tk.Label(root, text=f"Total Amount: £{total_amount:.2f}")
total_label.pack(pady=(0, padding))

button_show_category_popup = tk.Button(root, text="Calculate Total for Specific Category", command=show_category_popup)
button_show_category_popup.pack(pady=(0, padding))

category_total_label_popup = tk.Label(root, text="")
category_total_label_popup.pack(pady=(0, padding))

button_add_category = tk.Button(root, text="Add New Category", command=open_add_category_window)
button_add_category.pack(pady=(0, padding))

button_close = tk.Button(root, text="Close", command=close_program)
button_close.pack(pady=(0, padding))

root.mainloop()
