import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# --- Main Window ---
root = tk.Tk()
root.title('LP Tracker 0.9')
root.geometry('700x500')
root.resizable(False, False)

current_lp = 0
lp_history = []
lp_values = []
graph_displayed = False
graph_canvas = None

# --- Background Image ---
try:
    bg_image = Image.open("project/leaguetracker/images/singed.jpeg") 
    bg_image = bg_image.resize((700, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    print("Background image not found or failed to load.")

# --- Functions ---
def update_lp(amount):
    global current_lp
    current_lp += amount
    timestamp = datetime.now().strftime('%H:%M:%S')
    lp_history.append(f"[{timestamp}] {'+' if amount >= 0 else ''}{amount} LP")
    lp_values.append(current_lp)
    update_display()

def reset_lp():
    global current_lp, lp_history, lp_values
    current_lp = 0
    lp_history = []
    lp_values = []
    update_display()
    clear_graph()

def update_display():
    lp_label.config(text=f"Current LP: {current_lp}")
    history_text.delete(1.0, tk.END)
    for entry in reversed(lp_history[-10:]):
        history_text.insert(tk.END, entry + "\n")

def update_lp_from_entry():
    try:
        value = int(lp_entry.get())
        update_lp(value)
        lp_entry.delete(0, tk.END)
    except ValueError:
        lp_entry.delete(0, tk.END)
        lp_entry.insert(0, "Invalid")

def toggle_graph():
    global graph_displayed, graph_canvas

    if graph_displayed:
        # Hide the graph
        if graph_canvas:
            graph_canvas.get_tk_widget().destroy()
            graph_canvas = None
        graph_button.config(text="Show Graph")
        graph_displayed = False
    else:
        if not lp_values:
            return
        fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
        ax.plot(lp_values, marker='o', color='blue')
        ax.set_title("LP Over Time")
        ax.set_xlabel("Games")
        ax.set_ylabel("LP")

        graph_canvas = FigureCanvasTkAgg(fig, master=root)
        graph_canvas.get_tk_widget().place(x=400, y=270)
        graph_canvas.draw()
        graph_button.config(text="Hide Graph")
        graph_displayed = True

# --- Title ---
title_label = tk.Label(root, text="LP DIFF!", fg="white", bg="black", font=("Helvetica", 20, "bold"))
title_label.place(x=20, y=10)

# --- Current LP Display ---
lp_label = tk.Label(root, text="Current LP: 0", font=("Helvetica", 18, "bold"), fg="white", bg="black")
lp_label.place(x=20, y=50)

# --- Buttons --- (Smaller size and better background color)
def create_button(text, x, y, command):
    return tk.Button(root, text=text, width=12, height=1, command=command, bg="black", fg="white", 
                     font=("Helvetica", 10, "bold"), relief="flat", bd=2, highlightthickness=0,
                     activebackground="#333", activeforeground="white")

win_button = create_button("Win (+20 LP)", 20, 100, lambda: update_lp(20))
win_button.place(x=20, y=100)

loss_button = create_button("Loss (-15 LP)", 20, 130, lambda: update_lp(-15))
loss_button.place(x=20, y=130)

# --- Entry + Custom Button --- (Smaller and improved color)
lp_entry = tk.Entry(root, width=8, font=("Helvetica", 12), bg="black", fg="white", bd=2, relief="flat")
lp_entry.place(x=20, y=170)

custom_button = tk.Button(root, text="LP Change", width=12, height=1, command=update_lp_from_entry, bg="black", fg="white", 
                          font=("Helvetica", 10, "bold"), relief="flat", bd=2, highlightthickness=0, 
                          activebackground="#333", activeforeground="white")
custom_button.place(x=20, y=200)

# --- Reset & Graph Buttons --- (Smaller size and improved color)
reset_button = tk.Button(root, text="Reset LP", fg="red", command=reset_lp, bg="black", relief="flat", 
                         font=("Helvetica", 10, "bold"), activebackground="#333", activeforeground="white")
reset_button.place(x=20, y=240)

graph_button = tk.Button(root, text="Show Graph", command=toggle_graph, bg="black", fg="white", relief="flat", 
                         font=("Helvetica", 10, "bold"), activebackground="#333", activeforeground="white")
graph_button.place(x=20, y=270)

# --- History Log --- (Smaller and improved color)
history_label = tk.Label(root, text="History (Last 10):", font=("Helvetica", 12, "italic"), fg="white", bg="black")
history_label.place(x=20, y=320)

history_text = tk.Text(root, height=6, width=60, font=("Courier", 10), bg="black", fg="white", bd=2, relief="flat")
history_text.place(x=20, y=350)

# --- Start App ---
root.mainloop()
