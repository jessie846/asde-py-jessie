import tkinter as tk
from tkinter import filedialog
from geojson_viewer import GeoJSONViewer
from scrolling_bar import create_scrolling_bar

def load_geojson():
    file_path = filedialog.askopenfilename(filetypes=[("GeoJSON files", "*.geojson *.json")])
    if not file_path:
        return
    geojson_viewer.plot_geojson(file_path)

def toggle_day_night():
    geojson_viewer.toggle_day_night()

def scroll_both(event):
    if event.state & 0x0001:  # Check if Shift is pressed
        geojson_viewer.scroll(event)
    else:
        if event.delta:
            top_bar.xview_scroll(-int(event.delta / 120), "units")
        elif event.num == 5:
            top_bar.xview_scroll(1, "units")
        elif event.num == 4:
            top_bar.xview_scroll(-1, "units")

# Create the main application window
root = tk.Tk()
root.title("Custom Background GUI with GeoJSON Rendering")
root.geometry("800x600")
root.configure(bg="#005c73")

# Create the GeoJSON viewer
geojson_viewer = GeoJSONViewer(master=root)
geojson_viewer.grid(row=1, column=0, sticky="nsew")

# Create the top bar with two layers
top_bar = create_scrolling_bar(root, "#4c4c4c", "#606060", "#353535")

# Add the DAY/NITE button to the top layer
day_night_button = tk.Button(top_bar, text="DAY/NITE", command=toggle_day_night, bg="#333", fg="white")
day_night_button.grid(row=0, column=10, padx=10, sticky="e")  # Adjusted grid position

# Add a button to load the GeoJSON file
load_geojson_button = tk.Button(root, text="Load GeoJSON", command=load_geojson)
load_geojson_button.grid(row=2, column=0, pady=10, sticky="ew")

# Configure grid row and column weights
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Bind scrolling events
root.bind_all("<MouseWheel>", scroll_both)
root.bind_all("<Button-4>", scroll_both)
root.bind_all("<Button-5>", scroll_both)

# Run the application
root.mainloop()
