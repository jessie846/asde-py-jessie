import tkinter as tk

def create_scrolling_bar(parent, bg_color, box_bg_color, box_outline_color):
    bar = tk.Canvas(parent, bg=bg_color, height=100, highlightthickness=0)
    bar.grid(row=0, column=0, sticky="ew")  # Use grid instead of pack

    # Create top and bottom layers
    top_layer = tk.Frame(bar, bg=box_bg_color, height=50)
    top_layer.grid(row=0, column=0, sticky="ew")
    
    bottom_layer = tk.Frame(bar, bg=box_bg_color, height=50)
    bottom_layer.grid(row=1, column=0, sticky="ew")
    
    for i in range(10):
        label = tk.Label(top_layer, text=f"Item {i+1}", bg=box_outline_color, fg="white", padx=20, pady=5)
        label.grid(row=0, column=i, padx=2, pady=2, sticky="w")
        
    for i in range(10):
        label = tk.Label(bottom_layer, text=f"Item {i+1}", bg=box_outline_color, fg="white", padx=20, pady=5)
        label.grid(row=0, column=i, padx=2, pady=2, sticky="w")
    
    bar.update_idletasks()
    bar.configure(scrollregion=bar.bbox("all"))
    
    return bar
