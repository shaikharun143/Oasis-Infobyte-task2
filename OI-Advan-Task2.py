import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Database setup
def initialize_db():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

# BMI calculation
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# Save record to the database
def save_record(weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bmi_records (date, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
                   (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), weight, height, bmi, category))
    conn.commit()
    conn.close()

# Display BMI trend graph
def show_trend():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date, bmi FROM bmi_records")
    data = cursor.fetchall()
    conn.close()

    if data:
        dates = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') for record in data]
        bmi_values = [record[1] for record in data]

        plt.plot(dates, bmi_values, marker='o')
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.title("BMI Trend Over Time")
        plt.show()
    else:
        messagebox.showinfo("Information", "No BMI records found to display trend.")

# GUI setup
def calculate_and_display():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return
        
        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)

        label_result.config(text=f"Your BMI: {bmi:.2f}\nCategory: {category}")
        save_record(weight, height, bmi, category)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for weight and height.")

# Main application window
initialize_db()

app = tk.Tk()
app.title("BMI Calculator")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

# Weight input
label_weight = tk.Label(frame, text="Weight (kg):")
label_weight.grid(row=0, column=0, padx=5, pady=5)
entry_weight = tk.Entry(frame)
entry_weight.grid(row=0, column=1, padx=5, pady=5)

# Height input
label_height = tk.Label(frame, text="Height (m):")
label_height.grid(row=1, column=0, padx=5, pady=5)
entry_height = tk.Entry(frame)
entry_height.grid(row=1, column=1, padx=5, pady=5)

# Calculate button
button_calculate = tk.Button(frame, text="Calculate BMI", command=calculate_and_display)
button_calculate.grid(row=2, column=0, columnspan=2, pady=10)

# Result display
label_result = tk.Label(frame, text="")
label_result.grid(row=3, column=0, columnspan=2)

# Trend button
button_trend = tk.Button(frame, text="Show BMI Trend", command=show_trend)
button_trend.grid(row=4, column=0, columnspan=2, pady=10)

app.mainloop()
