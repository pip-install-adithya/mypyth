import mysql.connector
import random
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

config = {
    'user': 'root',
    'password': '#put_ur_password',
    'host': 'localhost',
    'database': 'school_timetable1',
    'raise_on_warnings': True
}

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
timetable = None

def fetch_subjects(table_name):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(f"SELECT subject_name, weekly_frequency FROM {table_name}")
    subjects = cursor.fetchall()
    cursor.close()
    db.close()
    return {subject[0]: subject[1] for subject in subjects}

def allocate_block_periods(timetable, main_subjects_freq, block_periods_subject, periods_per_day):
    block_day = random.choice([day for day in days if day != 'Saturday'])
    block_start_period = random.randint(1, periods_per_day[block_day] - 2)
    timetable[block_day].extend([block_periods_subject, block_periods_subject])
    main_subjects_freq[block_periods_subject] -= 2

def allocate_electives(timetable, elective_pool):
    for day in days:
        if elective_pool:
            elective = random.choice(elective_pool)
            timetable[day].append(elective)
            elective_pool.remove(elective)

def generate_timetable():
    global timetable
    if timetable is None:
        timetable = {day: [] for day in days}
        main_subjects_freq = fetch_subjects('main_subjects')
        elective_subjects_freq = fetch_subjects('elective_subjects')
        periods_per_day = {day: 9 for day in days}
        periods_per_day['Saturday'] = 4
        block_periods_subject = "Computer Science"
        allocate_block_periods(timetable, main_subjects_freq, block_periods_subject, periods_per_day)
        subjects_pool = [subject for subject, freq in main_subjects_freq.items() for _ in range(freq)]
        elective_pool = [subject for subject, freq in elective_subjects_freq.items() for _ in range(freq)]
        allocate_electives(timetable, elective_pool)
        for day in days:
            for subject in main_subjects_freq.keys():
                if subject in subjects_pool and len(timetable[day]) < periods_per_day[day] and timetable[day].count(subject) == 0:
                    timetable[day].append(subject)
                    subjects_pool.remove(subject)
        attempts = 0
        max_attempts = 20
        while len(timetable[day]) < periods_per_day[day] and attempts < max_attempts:
            subject = random.choice(subjects_pool)
            if timetable[day].count(subject) < 2 and (day != "Saturday" or (day == "Saturday" and subject not in timetable[day])):
                timetable[day].append(subject)
                subjects_pool.remove(subject)
            else:
                attempts += 1

def edit_period():
    global timetable
    response = simpledialog.askstring("Edit Period", "Do you want to edit a period? (yes or no)")
    if response and response.lower() == "yes":
        day = simpledialog.askstring("Edit Period", "Enter the day (e.g., Monday):")
        period = simpledialog.askinteger("Edit Period", "Enter the period (e.g., 1):")
        new_subject = simpledialog.askstring("Edit Period", "Enter the new subject:")
        if day and period and new_subject:
            if day in days and 1 <= period <= 9:
                timetable[day][period - 1] = new_subject
        edit_period()

def confirm_timetable():
    confirm_response = messagebox.askyesno("Confirm Timetable", "Do you want to confirm the timetable?")
    if confirm_response:
        display_confirmed_timetable()

def display_confirmed_timetable():
    confirmed_window = tk.Toplevel()
    confirmed_window.title("Confirmed Timetable")
    confirmed_columns = ['Day', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8', 'Period 9']
    confirmed_treeview = ttk.Treeview(confirmed_window, columns=confirmed_columns, show="headings")
    for col in confirmed_columns:
        confirmed_treeview.heading(col, text=col)
        confirmed_treeview.column(col, width=120)
    confirmed_treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    for day, subjects in timetable.items():
        row_data = [day]
        row_data.extend(subjects)
        while len(row_data) < len(confirmed_columns):
            row_data.append('')
        confirmed_treeview.insert('', 'end', values=row_data)
    confirm_button = ttk.Button(confirmed_window, text="Confirm", command=confirmed_window.destroy)
    confirm_button.pack(pady=20)
    confirmed_window.geometry("1050x500")

def display_edited_timetable(edited_timetable):
    edited_window = tk.Toplevel()
    edited_window.title("Edited Timetable")
    edited_columns = ['Day', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8', 'Period 9']
    edited_treeview = ttk.Treeview(edited_window, columns=edited_columns, show="headings")
    for col in edited_columns:
        edited_treeview.heading(col, text=col)
        edited_treeview.column(col, width=120)
    edited_treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    for day, subjects in edited_timetable.items():
        row_data = [day]
        row_data.extend(subjects)
        while len(row_data) < len(edited_columns):
            row_data.append('')
        edited_treeview.insert('', 'end', values=row_data)
    confirm_button = ttk.Button(edited_window, text="Confirm", command=edited_window.destroy)
    confirm_button.pack(pady=20)
    edited_window.geometry("1050x500")

def display_edited_timetable_button():
    if timetable is not None:
        display_edited_timetable(timetable)
    else:
        print("Timetable is not generated yet.")

def display_timetable():
    for row in treeview.get_children():
        treeview.delete(row)
    generate_timetable()
    for day, subjects in timetable.items():
        random.shuffle(subjects)
        row_data = [day]
        row_data.extend(subjects)
        while len(row_data) < len(columns):
            row_data.append('')
        treeview.insert('', 'end', values=row_data)

root = tk.Tk()
root.title("School Timetable")
generate_button = ttk.Button(root, text="Generate Timetable", command=display_timetable)
generate_button.pack(pady=20)
edit_button = ttk.Button(root, text="Edit Period", command=edit_period)
edit_button.pack(pady=20)
display_edited_button = ttk.Button(root, text="Display Edited Timetable", command=display_edited_timetable_button)
display_edited_button.pack(pady=20)
confirm_button = ttk.Button(root, text="Confirm Timetable", command=confirm_timetable)
confirm_button.pack(pady=20)
columns = ['Day', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8', 'Period 9']
treeview = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=120)
treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
root.geometry("1050x500")
root.mainloop()
