import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
import random

window = ttk.Window(themename="superhero")
windll.shcore.SetProcessDpiAwareness(1)
window.title('DM\'s Toolkit')
window.geometry("800x500")
window.minsize(width=800, height=500)

top_frame = tk.Frame(window, bg="#0C0C0C", height=20)
center_frame = tk.Frame(window)
right_frame = tk.Frame(window, bg="#202020", width=200)
bottom_frame = tk.Frame(window, bg="#0C0C0C", height=20)

hps = [[ttk.Entry(center_frame, width=7)]]
names = [ttk.Entry(center_frame, width=7)]

def new_hp_item():
    hp = [ttk.Entry(center_frame, width=10)]
    hps.append(hp)
    name = ttk.Entry(center_frame, width=10)
    names.append(name)
    update()

def update_hp_values(event):
    focus = window.focus_get()
    for i in hps:
        if focus in i:
            hps_list = i
            break
    else:
        if focus in names:
            idx = names.index(focus)
            names[idx].grid_forget()
            names[idx] = ttk.Label(center_frame, text=focus.get(), width=10)
            update()
        return
    
    txt = focus.get()
    if "-" in txt:
        txt = int(txt)
        new_hp = int(hps_list[-2]["text"])+txt
    elif "+" in txt:
        txt.strip("+")
        txt = int(txt)
        new_hp = int(hps_list[-2]["text"])+txt
    else:
        txt = int(txt)
        new_hp = txt
    hps_list.insert(-1, ttk.Label(center_frame, text=f"{new_hp}", width=10))
    hps_list[-1].delete(0,tk.END)
    update()

def stay_on_top():
    window.attributes('-topmost', not window.attributes('-topmost'))

die_size_box = ttk.Spinbox(bottom_frame, from_=1, to=100, width=5, takefocus=False)
die_number_box = ttk.Spinbox(bottom_frame, from_=1, to=100, width=5, takefocus=False)
label_d = ttk.Label(bottom_frame, text="d")
roll_display = ttk.Label(bottom_frame, text="")

def roll_dice():
    die_number = int(die_number_box.get())
    die_size = int(die_size_box.get())
    roll_list = []
    total = 0
    for i in range(die_number):
        roll = random.randint(1,die_size)
        roll_list.append(roll)
        total += roll
    roll_list = f"{roll_list}".replace("'", "").replace("[","(").replace("]",")")
    roll_display['text'] = f"{total} {roll_list}"
    die_size_box.delete(0,tk.END)
    die_number_box.delete(0,tk.END)
    update()

def resetItem():
    idx = select.current()
    names[idx].grid_forget()
    names[idx] = ttk.Entry(center_frame, width=10)
    for hp in hps[idx]:
        hp.grid_forget()
    hps[idx] = [ttk.Entry(center_frame, width=10)]
    update()
def killItem():
    idx = select.current()
    print(names[idx].cget("state"))
    if names[idx].cget("state") == "normal":
        names[idx].config(state="disabled")
        hps[idx][-1].config(state="disabled")
    else:
        names[idx].config(state="normal")
        hps[idx][-1].config(state="normal")
    update()

init_list = []
def add_init():
    global init_list
    for item in initiative.get_children():
        initiative.delete(item)
    if init_name.get() != "":
        name = init_name.get()
    else:
        name="Monster"
    if init_num.get() != "":
        num = init_num.get()
    else:
        num="0"
    item = {"name":name, "num":num}
    init_list.append(item)
    init_list = sorted(init_list, key=lambda n: n["num"], reverse=True)
    for init in init_list:
        initiative.insert("", "end",id=init_list.index(init), values=(init["name"], init["num"]))
    init_name.delete(0,tk.END)
    init_num.delete(0,tk.END)
    update()

selected=0
def reset_init():
    global init_list, selected
    for item in initiative.get_children():
      initiative.delete(item)
    init_list = []
    selected=0
    update()


def next_init():
    global selected
    if selected < len(initiative.get_children()):
        initiative.selection_set(selected)
        selected+=1
    elif len(initiative.get_children()) > 0:
        initiative.selection_set(0)
        selected=1
    else:
        pass
    

initiative = ttk.Treeview(right_frame, columns=("name", "init"), show="headings", selectmode="none", takefocus=False)
initiative.heading('name', text='Name')
initiative.heading('init', text="#")
initiative.column("name", width=160, stretch=tk.NO)
initiative.column("init", width=60, stretch=tk.NO)
initiative.bind('<Motion>', 'break')
init_name = ttk.Entry(right_frame, width=10, takefocus=False, bootstyle="info")
init_num = ttk.Spinbox(right_frame, width=7, from_=1, to=100, takefocus=False, bootstyle="info")
init_add = ttk.Button(right_frame, width=10, text="Add", command=add_init, takefocus=False, bootstyle="info-outline")
init_reset = ttk.Button(right_frame, width=10, text="Reset", command=reset_init, takefocus=False, bootstyle="info-outline")
init_next = ttk.Button(right_frame, width=24, text="Next",command=next_init, takefocus=False, bootstyle="info-outline")

window.bind("<Return>", update_hp_values)
new = ttk.Button(top_frame, text="New", command=new_hp_item, takefocus=False, width=10, style="success-outline")
quit = ttk.Button(top_frame, text="Quit", command=lambda:window.destroy(), takefocus=False, width=10, style="danger-outline")
top = ttk.Checkbutton(top_frame, text="Top", bootstyle="info-outline-toolbutton",  command=stay_on_top, takefocus=False, width=10)
select = ttk.Combobox(top_frame, width=10, takefocus=False, bootstyle="success")
reset = ttk.Button(top_frame, text="Reset", command=resetItem, takefocus=False, width=10, bootstyle="info-outline")
kill = ttk.Button(top_frame, text="Kill", command=killItem, takefocus=False, width=10, bootstyle="info-outline")
select["state"] = 'readonly'
def updateSelection():
    select_list = []
    for name in names:
        if type(name) == ttk.Label:
            select_list.append(name.cget("text"))
        elif type(name) == ttk.Entry:
            if name.get() != "":
                select_list.append(name.get())
            else:
                select_list.append(names.index(name)+1)
        else:
            select_list.append("null")
    select["values"] = select_list
updateSelection()

roll = ttk.Button(bottom_frame, text="Roll", command=roll_dice, takefocus=False, width=10, bootstyle="warning-outline")

def update():
    top_frame.pack(anchor="nw", expand=False, fill="x")
    right_frame.pack(anchor="nw", expand=False, fill="y", side=tk.RIGHT)
    center_frame.pack(anchor="nw", expand=True)
    bottom_frame.pack(anchor="sw", expand=False, fill="x")
    for hp in hps:
        for h in hp:
            h.grid(row=(hp.index(h)+1), column=hps.index(hp), sticky="NW", padx=10, pady=4)
    for name in names:
        name.grid(row=0, column=names.index(name), sticky="NW", padx=10, pady=10)

    quit.grid(row=0, column=0, sticky="NW", padx=10, pady=4)
    top.grid(row=0, column=1, sticky="NW", padx=10, pady=4)
    new.grid(row=0, column=2, sticky="NW", padx=10, pady=4)
    ttk.Separator(top_frame, orient="vertical").grid(row=0, column=3, sticky="NW", padx=15, pady=4)
    select.grid(row=0, column=4, sticky="NW", padx=10, pady=4)
    updateSelection()
    reset.grid(row=0, column=5, sticky="NW", padx=10, pady=4)
    kill.grid(row=0, column=6, sticky="NW", padx=10, pady=4)
    
    initiative.grid(row=0, column=0, sticky="NW", columnspan=2)
    ttk.Separator(right_frame, orient="horizontal").grid(row=1, column=0, columnspan=2, pady=10)
    init_name.grid(row=2, column=0, sticky="NW", padx=4, pady=4)
    ttk.Label(right_frame, text="Name").grid(row=2, column=1, sticky="W", padx=5)
    init_num.grid(row=3, column=0, sticky="NW", padx=4, pady=4)
    ttk.Label(right_frame, text="Initiative").grid(row=3, column=1, sticky="W", padx=5)
    init_add.grid(row=4, column=0, sticky="NW", padx=4, pady=10)
    init_reset.grid(row=4, column=1, sticky='NW', padx=2, pady=10)
    init_next.grid(row=5, column=0, sticky="NW", columnspan=2, padx=4)
    
    die_number_box.grid(row=0,column=0,sticky="SW", padx=10, pady=4)
    label_d.grid(row=0,column=1, sticky="SW", pady=8)
    die_size_box.grid(row=0,column=2,sticky="SW", padx=10, pady=4)
    roll.grid(row=0, column=5, sticky="SW", padx=5, pady=4)
    roll_display.grid(row=0, column=6, sticky="SW", pady=8)

update()
window.mainloop()