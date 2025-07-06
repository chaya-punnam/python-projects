import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os

login_file = "login.csv"
student_file = "students.csv"

def load_login_data():
    if not os.path.exists(login_file):
        with open(login_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])
            writer.writerow(["admin", "1234"])
    with open(login_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            return row["username"], row["password"]
    return "admin", "1234"

def update_login_data(new_username, new_password):
    with open(login_file, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password"])
        writer.writerow([new_username, new_password])

def show_login():
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("320x230")
    login_win.configure(bg="#2d0033")

    tk.Label(login_win, text="Username", bg="#2d0033", fg="white").pack(pady=5)
    username_entry = tk.Entry(login_win, width=25, bg="#33004d", fg="white")
    username_entry.pack()

    tk.Label(login_win, text="Password", bg="#2d0033", fg="white").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", width=25, bg="#33004d", fg="white")
    password_entry.pack()

    def validate_login():
        saved_user, saved_pass = load_login_data()
        username = username_entry.get()
        password = password_entry.get()

        if username == saved_user and password == saved_pass:
            login_win.destroy()
            show_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def change_credentials():
        new_user = simpledialog.askstring("Change Username", "Enter new username:")
        new_pass = simpledialog.askstring("Change Password", "Enter new password:", show="*")
        if new_user and new_pass:
            update_login_data(new_user, new_pass)
            messagebox.showinfo("Success", "Credentials updated successfully! Please restart the app to apply changes.")

    tk.Button(login_win, text="Login", command=validate_login, bg="#800080", fg="white").pack(pady=10)
    tk.Button(login_win, text="Change Username & Password", command=change_credentials, bg="#333366", fg="white").pack(pady=5)

    login_win.mainloop()

def calculate_average_and_grade(marks):
    avg = sum(marks) / len(marks)
    if avg >= 90:
        grade = 'A'
    elif avg >= 75:
        grade = 'B'
    elif avg >= 60:
        grade = 'C'
    elif avg >= 50:
        grade = 'D'
    else:
        grade = 'F'
    return avg, grade

def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    branch = branch_entry.get().strip()

    if not name or not roll or not branch:
        messagebox.showerror("Error", "Please enter name, roll number, and branch.")
        return

    if os.path.exists(student_file):
        with open(student_file, "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row and row[0] == roll:
                    messagebox.showerror("Duplicate Roll", f"Roll number '{roll}' already exists!")
                    return

    try:
        num_subjects = int(subjects_entry.get())
        if num_subjects <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Please enter a valid number of subjects.")
        return

    marks = []
    for i in range(num_subjects):
        mark = simpledialog.askfloat("Enter Marks", f"Enter marks for Subject {i+1}:", minvalue=0, maxvalue=100)
        if mark is None:
            return
        marks.append(mark)

    avg, grade = calculate_average_and_grade(marks)
    student = [roll, name, branch, num_subjects, round(avg, 2), grade]
    save_to_file(student)

    messagebox.showinfo("Success", f"Student {name} added successfully!")
    clear_entries()

def save_to_file(student):
    write_header = not os.path.exists(student_file) or os.path.getsize(student_file) == 0
    with open(student_file, "a", newline='') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Roll", "Name", "Branch", "Subjects", "Average", "Grade"])
        writer.writerow(student)

def display_students():
    window = tk.Toplevel(root)
    window.title("All Student Records")
    window.configure(bg="#1a001a")

    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("Treeview", background="#2d0033", foreground="white",
                    rowheight=30, fieldbackground="#2d0033", font=('Arial', 11))
    style.map('Treeview', background=[('selected', '#a64ca6')])

    columns = ("Roll", "Name", "Branch", "Subjects", "Average", "Grade")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    if not os.path.exists(student_file):
        messagebox.showinfo("Info", "No student records found.")
        return

    with open(student_file, "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row:
                tree.insert("", tk.END, values=row)

def delete_student():
    roll_to_delete = simpledialog.askstring("Delete Student", "Enter Roll Number to delete:")

    if not roll_to_delete:
        return

    if not os.path.exists(student_file):
        messagebox.showerror("Error", "No student data found!")
        return

    updated_students = []
    found = False

    with open(student_file, "r") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
            if row and row[0] != roll_to_delete:
                updated_students.append(row)
            else:
                found = True

    if not found:
        messagebox.showinfo("Not Found", f"No student found with roll number {roll_to_delete}")
        return

    with open(student_file, "w", newline='') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(header)
        writer.writerows(updated_students)

    messagebox.showinfo("Deleted", f"Student with Roll Number {roll_to_delete} deleted successfully!")

def clear_entries():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    subjects_entry.delete(0, tk.END)

def show_main_app():
    global root, name_entry, roll_entry, branch_entry, subjects_entry

    root = tk.Tk()
    root.title("Student Grade Management System")
    root.geometry("600x460")
    root.configure(bg="#1a001a")

    tk.Label(root, text="Student Grade Management", font=("Helvetica", 16, "bold"), fg="#e0b3ff", bg="#1a001a").pack(pady=10)

    tk.Label(root, text="Name:", fg="white", bg="#1a001a").pack()
    name_entry = tk.Entry(root, width=40, bg="#33004d", fg="white", insertbackground="white")
    name_entry.pack(pady=3)

    tk.Label(root, text="Roll Number:", fg="white", bg="#1a001a").pack()
    roll_entry = tk.Entry(root, width=40, bg="#33004d", fg="white", insertbackground="white")
    roll_entry.pack(pady=3)

    tk.Label(root, text="Branch:", fg="white", bg="#1a001a").pack()
    branch_entry = tk.Entry(root, width=40, bg="#33004d", fg="white", insertbackground="white")
    branch_entry.pack(pady=3)

    tk.Label(root, text="Number of Subjects:", fg="white", bg="#1a001a").pack()
    subjects_entry = tk.Entry(root, width=40, bg="#33004d", fg="white", insertbackground="white")
    subjects_entry.pack(pady=3)

    button_frame = tk.Frame(root, bg="#1a001a")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Add", command=add_student, bg="#800080", fg="white", width=12).grid(row=0, column=0, padx=6)
    tk.Button(button_frame, text="Show", command=display_students, bg="#660066", fg="white", width=12).grid(row=0, column=1, padx=6)
    tk.Button(button_frame, text="Delete", command=delete_student, bg="#cc0066", fg="white", width=12).grid(row=0, column=2, padx=6)
    tk.Button(button_frame, text="Exit", command=root.destroy, bg="#99004d", fg="white", width=12).grid(row=0, column=3, padx=6)

    root.mainloop()

show_login()
