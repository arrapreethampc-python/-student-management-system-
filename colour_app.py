import tkinter as tk
import csv
from tkinter import messagebox

students = []

root = tk.Tk()
root.title("Student Manager")
root.geometry("500x500")
root.configure(bg="#1e1e2f")


title = tk.Label(root, text="Student Manager", bg="#1e1e2f", fg="white",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)


tk.Label(root, text="Name", bg="#1e1e2f", fg="white").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)


tk.Label(root, text="Marks", bg="#1e1e2f", fg="white").pack()
marks_entry = tk.Entry(root, width=30)
marks_entry.pack(pady=5)


output = tk.Listbox(root, height=10, width=40, bg="#2e2e3e", fg="white")
output.pack(pady=10)



def sorted_student():
    students.sort(key=lambda x: x['marks'],reverse=True)
    view_students()

def get_grade(marks):
    marks = int(marks)
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 50:
        return 'C'
    else:
        return 'Fail'

def export_csv():
    if not students:
        output.insert(tk.END,'no data to export')
        return
    output.delete(0,tk.END)
    
    with open('students.csv','w', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['name','marks','Grade'])
        
        for student in students:
            grade=get_grade(student['marks'])
            writer.writerow([student['name'],student['marks'],grade])
            
    output.insert(tk.END,'exported to students.csv')
    
def add_student():
    name = name_entry.get()
    if name == '':
        output.insert(tk.END,'name cannot be empty')
        return
    try:
        marks = int(marks_entry.get())
    except:
        output.insert(tk.END, "Enter valid marks")
        return

    students.append({"name": name, "marks": marks})
    output.insert(tk.END, f"Added: {name}\n")

    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

    save_student()
    return

def view_students():
    output.delete(0, tk.END)
    
    sorted_student=sorted(students,key=lambda x: x['marks'],reverse=True)
    rank=1
    for s in sorted_student:
        grade = get_grade(s["marks"])
        output.insert(tk.END,
            f'Rank {rank}{s["name"]} - {s["marks"]} - {grade}')
        rank+=1
    
def show_topper():
    output.delete(0, tk.END)

    if not students:
        output.insert(tk.END, "No students available")
        return

    topper = students[0]

    for student in students:
        if student['marks'] > topper['marks']:
            topper = student

    grade = get_grade(topper['marks'])

    output.insert(tk.END,
        f'Topper: {topper["name"]} - {topper["marks"]} - Grade: {grade}')


def search_student():
    name = name_entry.get()
    output.delete(0, tk.END)

    for student in students:
        if student['name'].lower() == name.lower():
            grade = get_grade(student['marks'])
            output.insert(tk.END,
                f'Found: {student["name"]} - {student["marks"]} - Grade: {grade}')
            name_entry.delete(0, tk.END)
            return

    output.insert(tk.END, 'Student not found')
    name_entry.delete(0, tk.END)

def live_search(event):
    text=name_entry.get().lower()
    output.delete(0,tk.END)
    for student in students:
        if text in student['name'].lower():
            grade=get_grade(student['marks'])
            output.insert(tk.END,f'{student["name"]} - {student["marks"]}')
name_entry.bind('<KeyRelease>',live_search)

def select_student(event):
    try:
        index = output.curselection()[0]
        student = students[index]

        name_entry.delete(0, tk.END)
        name_entry.insert(0, student['name'])

        marks_entry.delete(0, tk.END)
        marks_entry.insert(0, student['marks'])
    except:
        pass

output.bind("<<ListboxSelect>>", select_student)

def delete_student():
    if not students:
        output.insert(tk.END,'no data to delete')
        return
    try:
        selected_index = output.curselection()[0]
    except:
        output.insert(tk.END, 'Select a student first')
        return

    students.pop(selected_index)
    
    confirm=messagebox.askyesno('confirm','Delete this student')
    if not confirm:
        return
    save_student()
    view_students()
    
    
def update_marks():
    name = name_entry.get()

    for student in students:
        if student['name'].lower() == name.lower():
            try:
                marks = int(marks_entry.get())
            except:
                output.insert(tk.END, "Enter valid marks")
                return

            student['marks'] = marks
            save_student()
            view_students()
            return
    name_entry.delete(0,tk.END)
    marks_entry.delete(0,tk.END)
    output.insert(tk.END, 'Student not found')

    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


def save_student():
    print('saving')
    with open('colour_student.txt', "w") as file:
        for student in students:
            file.write(f'{student["name"]},{student["marks"]}\n')


def load_students():
    students.clear()
    try:
        with open('colour_student.txt', 'r') as file:
            for line in file:
                name, mark = line.strip().split(',')
                students.append({"name": name, "marks": int(mark)})
    except:
        pass




btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=10, bg="#4CAF50", fg="white",
          command=add_student).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="View", width=10, bg="#2196F3", fg="white",
          command=view_students).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text='Search', width=10, bg='#ff9800', fg='white',
          command=search_student).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text='Delete', width=10, bg='#f44336', fg='white',
          command=delete_student).grid(row=1, column=0, padx=5)

tk.Button(btn_frame, text='Update', width=10, bg='#9C27B0', fg='white',
          command=update_marks).grid(row=1, column=1, padx=5)

tk.Button(btn_frame, text='Topper', width=10, bg='#673AB7', fg='white',
          command=show_topper).grid(row=1, column=2, padx=5)

tk.Button(btn_frame, text='export CSV', width=20, bg='#009688',fg='white',command=export_csv).grid(row=2, column=0,columnspan=3, pady=5)


load_students()
root.mainloop()