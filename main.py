from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient()
db = client['usersdb2']
collection = db['users']

root = Tk()
root.title("MongoDB  Tkinter")
root.geometry("600x500")

columns = ("ID", "Name", "Age", "City")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill=BOTH, expand=True)

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Name").grid(row=0, column=0)
name_entry = Entry(frame)
name_entry.grid(row=0, column=1)

Label(frame, text="Age").grid(row=0, column=2)
age_entry = Entry(frame)
age_entry.grid(row=0, column=3)

Label(frame, text="City").grid(row=0, column=4)
city_entry = Entry(frame)
city_entry.grid(row=0, column=5)


def refresh():
    tree.delete(*tree.get_children())
    for doc in collection.find():
        tree.insert("", END, values=(str(doc["_id"]), doc["name"], doc["age"], doc["city"]))

    count =collection.count_documents({})

    if count==1:
        count_label.config(text = f"There is 1 doc in usersdb2's db users collection.")
    elif count==0:
        count_label.config(text=f"There is no docs in usersdb2's db users collection.")
    else:
        count_label.config(text=f"There are {count} docs in usersdb2's db users collection.")


def clear():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    city_entry.delete(0, END)

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()

    if name and age and city:
        collection.insert_one({"name": name, "age": age, "city": city})
        refresh()
        clear()
    else:
        showwarning(message="No data to add.")


def update_student():
    selected = tree.selection()
    if selected:
        item = tree.item(selected)
        _id = item["values"][0]
        name = name_entry.get()
        age = age_entry.get()
        city = city_entry.get()

        collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": {"name": name, "age": age, "city": city}}
        )
        refresh()
        clear()
    else:
        showwarning(message="No selections")


def delete_student():
    selected = tree.selection()
    if selected:
        item = tree.item(selected)

        _id = item["values"][0]

        collection.delete_one({"_id":ObjectId(_id)})

        refresh()
        clear()
    else:
        showwarning(message="No selections")

def on_item_select(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected)
        values = item["values"]
        name_entry.delete(0, END)
        name_entry.insert(0, values[1])
        age_entry.delete(0, END)
        age_entry.insert(0, values[2])
        city_entry.delete(0, END)
        city_entry.insert(0, values[3])


button_frame = Frame(root)
button_frame.pack(pady=10)

Button(button_frame, text="Add", command=add_student).grid(row=0, column=0, padx=5)
Button(button_frame, text="Update", command=update_student).grid(row=0, column=1, padx=5)
Button(button_frame, text="Delete", command=delete_student).grid(row=0, column=2, padx=5)
count_label = Label()
count_label.pack()

tree.bind("<<TreeviewSelect>>", on_item_select)

refresh()

root.mainloop()