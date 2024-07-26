import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import requests
import pyperclip
from PIL import ImageTk, Image
import urllib.request
import io
import webbrowser


recipe_current_index = 0

def clear_list(item_frame, item_list, item_price, cost_label):
    clear_list_approval = tk.messagebox.askyesno("Confirmation", "Do you wish to clear your recipe list?")
    if clear_list_approval:
        item_list.clear()
        item_price.clear()
        cost_label.config(text=f"Total Cost: ${sum(item_price):.2f}")
        update_item_buttons(item_frame=item_frame, name_list=item_list, price_list=item_price)


def search_recipes(app_id, app_key, query):
    url = f"https://api.edamam.com/search"
    params = {"q": query, "app_id": app_id, "app_key": app_key, "to": 5}
    response = requests.get(url, params=params)
    data = response.json()
    return data["hits"]

def update_item_buttons(item_frame, name_list, price_list):
    for widget in item_frame.winfo_children():
        widget.destroy()
    for name, price in zip(name_list, price_list):
        item_label = tk.Label(
            master=item_frame,
            text=f"{name}, ${price:.2f}",
            font=("Segoe UI", 19),  
            padx=10,
            pady=5,
            anchor="w", 
            bg=item_frame.cget("bg"),
            cursor="hand2" 
        )
        item_label.bind("<Button-1>", lambda e, n=name: remove_item(n, name_list, price_list, item_frame))
        item_label.pack(fill="x", padx=10, pady=2)


def remove_item(item_name, name_list, price_list, item_frame):
    confirm = tk.messagebox.askyesno("Confirmation", f"Do you wish to remove '{item_name}' from your recipe list?")
    if confirm:
        index = name_list.index(item_name)
        del name_list[index]
        del price_list[index]
        update_item_buttons(item_frame, name_list, price_list)

def clear_placeholder(event):
    if event.widget.get() in ("Enter name of food item here", "Enter price of food item here"):
        event.widget.delete(0, tk.END)

def recipes(input_list, index, title):
    global recipe_current_index
    if len(input_list) >= 2:
        api_id = "7a51ad65"
        api_key = "4326e6b4ad8c8be6e9c585476b593620"
        new_window = tk.Toplevel()
        new_window.geometry("400x600")
        new_window.title(title)
        new_window.resizable(height=True, width=False)

        name = []
        link = []
        image_link = []
        query = ', '.join(input_list)
        recipes = search_recipes(app_id=api_id, app_key=api_key, query=query)
        for i in recipes:
            recipe = i["recipe"]
            image_link.append(recipe["image"])
            name.append(f"{recipe['label']} ({recipe['source']})")
            link.append(recipe['url'])

        def widget(ind):
            global recipe_current_index
            image_frame = tk.Frame(master=new_window)
            image_frame.pack(padx=10, pady=10)
            if ind not in range(len(name)):
                ind = 0
                recipe_current_index = 0

            with urllib.request.urlopen(image_link[ind]) as a:
                data = a.read()
            
            image = Image.open(io.BytesIO(data))
            photo = ImageTk.PhotoImage(image)
            recipe_image = tk.Label(master=image_frame)
            recipe_image.image = photo  
            recipe_image.config(image=photo)
            recipe_image.pack(fill="both")

            recipe_frame = tk.Frame(master=new_window)
            recipe_frame.pack(padx=10, pady=10, fill="both")

            recipe_label = tk.Label(master=recipe_frame, wraplength=350, text=f"Recipe: {name[ind]} \n Link: {link[ind]}")
            recipe_label.pack(padx=10)
            
            button_frame = tk.Frame(master=new_window)
            button_frame.pack(padx=10, pady=10, fill="both")

            recipe_copy = tk.Button(master=button_frame, text="Copy", command=lambda:pyperclip.copy(link[ind]))
            recipe_copy.pack()

            recipe_open = tk.Button(master=button_frame, text="Open", command=lambda:webbrowser.open(url=link[ind]))
            recipe_open.pack()

            recipe_next = tk.Button(master=button_frame, text="New Recipe", command=lambda:next_recipe(window=new_window))
            recipe_next.pack()

            recipe_close = tk.Button(master=button_frame, text="Close Recipe", command=lambda:new_window.destroy())
            recipe_close.pack()

        widget(ind=index)

        def next_recipe(window):
            global recipe_current_index
            if len(name) == 0:  
                return

            for wid in window.winfo_children():
                wid.destroy()

            if recipe_current_index >= len(name) - 1:
                recipe_current_index = 0
            else:
                recipe_current_index += 1
            
            window.title(f"Recipe {recipe_current_index + 1}")
            widget(ind=recipe_current_index)


    else:
        tkinter.messagebox.showerror(message="You must have at least 2 food items in your recipe list to search for a recipe!")

def main():
    global recipe_current_index
    item_list = []
    item_price = []

    window = tk.Tk()
    window.geometry("350x600")
    window.title("Recipe List")
    window.resizable(height=False, width=False)

    title_label = tk.Label(master=window, text="Recipe List", font="Roboto 24 bold")
    title_label.pack(side='top', pady=10)

    price_label = tk.Label(master=window, text=f"Total Cost: $0.0", font="Aptos 15")
    price_label.pack(side="top", padx=5, pady=2)

    add_frame = tk.Frame(master=window)
    add_frame.pack(padx=10, pady=10)

    canvas_frame = tk.Frame(master=window)
    canvas_frame.pack(fill="both", expand=True, pady=(5, 5))

    canvas = tk.Canvas(master=canvas_frame, height=200)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(master=canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    button_frame = tk.Frame(master=canvas)
    canvas.create_window((0, 0), window=button_frame, anchor="n")
    button_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.configure(yscrollcommand=scrollbar.set)

    name_entry = tk.Entry(master=add_frame, font="Roboto 20")
    name_entry.insert(0, "Enter name of food item here")
    name_entry.bind("<FocusIn>", clear_placeholder)
    name_entry.pack(padx=10)

    price_entry = tk.Entry(master=add_frame, font="Roboto 20")
    price_entry.insert(0, "Enter price of food item here")
    price_entry.bind("<FocusIn>", clear_placeholder)
    price_entry.pack(padx=10)

    def name_price_append(name_entry, price_entry, name_list, price_list, item_frame, window, price_label):
        name = name_entry.get()
        print(name)
        price = price_entry.get()
        join_name = name.replace(" ", "")
        error = False

        float_check = price.replace('.', '', 1).isdigit()

        if name == "" or price == "" or name == "Enter name of food item here" or price == "Enter price of food item here":
            tkinter.messagebox.showerror(message="Must enter item name and price to add item to list!")
            error = True
        else:
            if name in name_list:
                tkinter.messagebox.showerror(message="Item already in Recipe list!")
                error = True
            if not join_name.isalpha():
                tkinter.messagebox.showerror(message="Item name must be only composed of alphabets!")
                error = True
            if not price.isnumeric() and not float_check:
                tkinter.messagebox.showerror(message="Price must be only composed of numbers and cannot have spaces!")
                error = True
            
        if not error:
            name_list.append(name.capitalize())
            price_list.append(float(price))
            name_entry.delete(0, tk.END)
            name_entry.insert(0, "Enter name of food item here")

            price_entry.delete(0, tk.END)
            price_entry.insert(0, "Enter price of food item here")
            
            price_label.config(text=f"Total Cost: ${sum(price_list):.2f}")

            update_item_buttons(item_frame, name_list, price_list)
            window.focus_set()

    add_button = tk.Button(master=add_frame, text="Add Item",
                           command=lambda: name_price_append(name_entry=name_entry, price_entry=price_entry, name_list=item_list, price_list=item_price, item_frame=button_frame, window=window, price_label=price_label))
    add_button.pack(side="top", pady=10)

    clear_button = tk.Button(master=window, text="Clear list",
                           command=lambda: clear_list(item_frame=button_frame, item_list=item_list, item_price=item_price, cost_label=price_label))
    clear_button.pack(side="bottom", pady=10)

    recipe_button = tk.Button(master=window, text="Search for Recipes",
                           command=lambda: recipes(input_list=item_list, index=recipe_current_index, title="Recipe 1"))
    recipe_button.pack(side="bottom")

    window.mainloop()

main()
