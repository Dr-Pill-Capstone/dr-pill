import csv
import time
import tkinter as tk
import api.open_cv as open_cv

def add_prescription():
    pill_name = name_entry.get()
    pill_qty = qty_entry.get()
    interval_num = interval_entry.get()
    interval_duration = duration_entry.get()
    start_time = start_entry.get()
    
    with open('dispensing_schedule.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pill_name, pill_qty, interval_num, interval_duration, start_time])
        
        name_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        interval_entry.delete(0, tk.END)
        duration_entry.delete(0, tk.END)
        start_entry.delete(0, tk.END)

def scan_bottle():
    scanner = open_cv.OpenCV()
    data = scanner.execute_scan()
    print(data)
    pill_qty = data[0]
    interval_num = data[1]
    interval_duration = data[2]
    pill_name = name_entry.get()
    start_time = start_entry.get()
    # name_entry.delete(0, tk.END)
    name_entry.insert(0, pill_name)
    # qty_entry.delete(0, tk.END)
    qty_entry.insert(0, pill_qty)
    # interval_entry.delete(0, tk.END)
    interval_entry.insert(0, interval_num)
    # duration_entry.delete(0, tk.END)
    duration_entry.insert(0, interval_duration)
    # start_entry.delete(0, tk.END)
    start_entry.insert(0, start_time)

window = tk.Tk()
window.title("Prescription Schedule")
window.geometry("400x200")

menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Entry Method", menu=file_menu)

file_menu.add_command(label="Manual Entry", command=lambda: scan_button.config(state="disabled"))

file_menu.add_command(label="Scan Bottle", command=lambda: scan_button.config(state="normal"))

name_label = tk.Label(window, text="Medicine:")
name_label.grid(column=0, row=0, padx=5, pady=5)
name_entry = tk.Entry(window)
name_entry.grid(column=1, row=0, padx=5, pady=5)

qty_label = tk.Label(window, text="Quantity:")
qty_label.grid(column=0, row=1, padx=5, pady=5)
qty_entry = tk.Entry(window)
qty_entry.grid(column=1, row=1, padx=5, pady=5)

interval_label = tk.Label(window, text="Interval Number:")
interval_label.grid(column=0, row=2, padx=5, pady=5)
interval_entry = tk.Entry(window)
interval_entry.grid(column=1, row=2, padx=5, pady=5)

duration_label = tk.Label(window, text="Interval Duration:")
duration_label.grid(column=0, row=3, padx=5, pady=5)
duration_entry = tk.Entry(window)
duration_entry.grid(column=1, row=3, padx=5, pady=5)

start_label = tk.Label(window, text="Schedule Start Time:")
start_label.grid(column=0, row=4, padx=5, pady=5)
start_entry = tk.Entry(window)
start_entry.grid(column=1, row=4, padx=5, pady=5)

add_button = tk.Button(window, text="Add Prescription", command=add_prescription)
add_button.grid(column=0, row=5, padx=5, pady=5)

scan_button = tk.Button(window, text="Scan Bottle", state="disabled", command=scan_bottle)
scan_button.grid(column=1, row=5, padx=5, pady=5)

window.mainloop()






