import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

TASK_FILE = "tasks.json"

# 1. load task from file if exist
if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r") as file:
        tasks = json.load(file)
else:
    tasks = []

# 2. Determine next task ID
task_id_counter = max([task["ID"] for task in tasks], default=0) + 1

# 3. function to save task
def save_task():
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# 4. function to add task
def add_task():
    global task_id_counter

    # 4.1 fetch details using get()
    title = title_entry.get()
    description = desc_entry.get()
    due_date = due_date_entry.get()

    # 4.2 warning to fill details 
    if not title or not description or not due_date:
        messagebox.showwarning("Input Error", "Please fill out all fields")
        return
    
    # 4.3 Prompts user to enter
    task = {
        "ID": task_id_counter,
        "Title": title,
        "Description": description,
        "Due_Date": due_date,
        "Status": "Pending"
    }
    tasks.append(task)
    task_id_counter += 1

    # 4.4 calling save function to save details
    save_task()

    # 4.5 display details 
    messagebox.showinfo("Task Added", f"Task successfully added!\n\n"
                        f"ID: {task['ID']}\n"
                        f"Title: {task['Title']}\n"
                        f"Description: {task['Description']}\n"
                        f"Due_Date: {task['Due_Date']}\n"
                        f"Status: {task['Status']}")
    
    # 4.6 clear the fields
    title_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)

# 5. function to view task
def view_tasks():
    # 5.1 new window for viewing tasks
    view_win = tk.Toplevel(root)
    view_win.title("All Tasks")
    view_win.geometry("700x300")

    # 5.2 treeview widget (table)
    columns = ("ID", "Title", "Description", "Due_Date", "Status")
    tree = ttk.Treeview(view_win, columns=columns, show="headings")

    # 5.3 define headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # 5.4 Define row tags (colors)
    tree.tag_configure("pending", foreground="red")
    tree.tag_configure("completed", foreground="green")

    # 5.5 insert tasks into table
    for task in tasks:
        status_tag = "pending" if task["Status"].lower() == "pending" else "completed"
        tree.insert(
            "",tk.END, values=(task["ID"], task["Title"], task["Description"], task["Due_Date"], task["Status"]),
            tags=(status_tag)
        )
    tree.pack(expand=True, fill="both")

    # 5.6 button to update task
    update_btn = tk.Button(view_win, text="Update Task", command=lambda: update_task(tree, view_win))
    update_btn.pack(pady=10)

# 6. function to update task
def update_task(tree, view_win):

    # 6.1 User selects a task from the table.
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("selection Error", "Please Please select a task to update.")
        return
    
    task_values = tree.item(selected_item[0], "values")
    task_id = int(task_values[0])

    # 6.2 find task in list
    task = next((t for t in tasks if t["ID"] == task_id), None)
    if not task:
        messagebox.showerror("Error", "Task not found.")
        return
    
    # 6.3 open update form
    update_win = tk.Toplevel(view_win)
    update_win.title("Update Task")
    update_win.geometry("400x250")

    tk.Label(update_win, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_entry_u = tk.Entry(update_win, width=30)
    title_entry_u.grid(row=0, column=1, padx=5, pady=5)
    title_entry_u.insert(0, task["Title"])

    tk.Label(update_win, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    desc_entry_u = tk.Entry(update_win, width=30)
    desc_entry_u.grid(row=1, column=1, padx=5, pady=5)
    desc_entry_u.insert(0, task["Description"])

    tk.Label(update_win, text="Due_Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    due_date_entry_u = tk.Entry(update_win, width=30)
    due_date_entry_u.grid(row=2, column=1, padx=5, pady=5)
    due_date_entry_u.insert(0, task["Due_Date"])

    tk.Label(update_win, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    status_var = tk.StringVar(value=task["Status"])
    status_dropdown = ttk.Combobox(update_win, textvariable=status_var, values=["Pending", "Completed"])
    status_dropdown.grid(row=3, column=1, padx=5, pady=5)

    # 6.4 After editing, user clicks Save:
    def save_update():
        task["Title"] = title_entry_u.get()
        task["Description"] = desc_entry_u.get()
        task["Due_Date"] = due_date_entry_u.get()  
        task["Status"] = status_var.get()

        save_task()
        # refresh Treeview
        tree.delete(*tree.get_children())
        for t in tasks:
            tag = "pending" if t["Status"].lower() == "pending" else "completed"
            tree.insert("", tk.END, values=(t["ID"], t["Title"], t["Description"], t["Due_Date"], t["Status"]), tags=(tag,))
        update_win.destroy()
        messagebox.showinfo("Success", f"Task {task_id} updated successfully.")
    tk.Button(update_win, text="Save", command=save_update).grid(row=4, column=0, columnspan=2, pady=10)

# create window
root = tk.Tk()
root.title("Task Manager")

# label for title
tk.Label(root, text="Task Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=5, pady=5)

# label for description
tk.Label(root, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
desc_entry = tk.Entry(root, width=40)
desc_entry.grid(row=1, column=1, padx=5, pady=5)

# lebel for Date
tk.Label(root, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
due_date_entry = tk.Entry(root, width=40)
due_date_entry.grid(row=2, column=1, padx=5, pady=5)

# add task button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# view task button
view_button = tk.Button(root, text="View All Tasks", command=view_tasks)
view_button.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
