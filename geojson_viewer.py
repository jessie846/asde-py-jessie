import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import geopandas as gpd

class GeoJSONViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.current_file_path = None
        self.day_mode = True  # Start with day mode by default
        self.figure = None
        self.ax = None
        self.canvas = None
        self.plot_area = None
        self.colors = {}
        self.zoom_scale = 1.1  # Zoom scale factor

        self.create_widgets()
        self.update_colors()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self, bg="#005c73")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = plt.Figure(dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')  # Hide axes completely
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.plot_area = self.canvas.get_tk_widget()

        self.bind_events()

    def update_colors(self):
        if self.day_mode:
            self.colors = {
                "apron": "#11345d",
                "building": "#203c62",  # Day mode color for building
                "taxiway": "#10254c",
                "structure": "#203c62",  # Day mode color for structure
                "background": "#393939"
            }
        else:
            self.colors = {
                "apron": "#464646",
                "building": "#606060",  # Night mode color for building
                "taxiway": "#2d2d2d",
                "structure": "#606060",  # Night mode color for structure
                "background": "#005c73"
            }
        if self.current_file_path:
            self.plot_geojson(self.current_file_path)  # Refresh the plot with new colors

    def plot_geojson(self, file_path):
        self.current_file_path = file_path  # Store file path for refresh
        try:
            gdf = gpd.read_file(file_path)

            self.ax.clear()  # Clear previous plots
            self.ax.axis('off')  # Make sure axes are hidden

            # Plot without altering aspect ratio
            gdf.plot(ax=self.ax, color=gdf.apply(lambda row: self.get_color(row), axis=1))
            self.ax.set_facecolor(self.colors['background'])
            self.ax.patch.set_facecolor(self.colors['background'])
            self.figure.patch.set_facecolor(self.colors['background'])

            # Set the limits based on the GeoJSON bounds
            self.ax.set_xlim(gdf.total_bounds[[0, 2]])
            self.ax.set_ylim(gdf.total_bounds[[1, 3]])

            # Set the axes to fill the entire plot area
            self.ax.set_position([0, 0, 1, 1])  # Use the entire figure for the plot

            # Maintain aspect ratio
            self.ax.set_aspect('equal', adjustable='datalim')

            self.canvas.draw()
        except Exception as e:
            print(f"An error occurred while plotting GeoJSON data: {e}")

    def get_color(self, row):
        color_map = {
            "apron": self.colors["apron"],
            "building": self.colors["building"],
            "taxiway": self.colors["taxiway"],
            "structure": self.colors["structure"],
            "runway": "#000000"  # Default color for runway, not changed
        }
        return color_map.get(row['asdex'], 'grey')

    def plot_aircraft_data(self, aircraft_data):
        try:
            self.ax.clear()  # Clear previous plots
            self.ax.axis('off')

            # Plot GeoJSON data if available
            if self.current_file_path:
                gdf = gpd.read_file(self.current_file_path)
                gdf.plot(ax=self.ax, color=gdf.apply(lambda row: self.get_color(row), axis=1))

            # Plot aircraft data
            for aircraft in aircraft_data:
                print(aircraft)  # Debugging: Print the aircraft data to see its structure

                lat = aircraft.get('lat')
                lon = aircraft.get('lon')
                callsign = aircraft.get('flight', aircraft.get('r', 'N/A')).strip()

                self.ax.plot(lon, lat, 'ro', markersize=5)  # Red dot for aircraft

                # Add text for the aircraft callsign
                self.ax.text(lon, lat, callsign, fontsize=8, color='white')

            self.ax.set_facecolor(self.colors['background'])
            self.ax.patch.set_facecolor(self.colors['background'])
            self.figure.patch.set_facecolor(self.colors['background'])

            # Maintain aspect ratio
            self.ax.set_aspect('equal', adjustable='datalim')

            self.canvas.draw()
        except Exception as e:
            print(f"An error occurred while plotting aircraft data: {e}")

    def toggle_day_night(self):
        self.day_mode = not self.day_mode
        self.update_colors()

    def bind_events(self):
        self.plot_area.bind("<MouseWheel>", self.scroll)
        self.plot_area.bind("<ButtonPress-1>", self.on_click)
        self.plot_area.bind("<B1-Motion>", self.on_drag)

    def scroll(self, event):
        if event.delta > 0:
            scale_factor = self.zoom_scale
        else:
            scale_factor = 1 / self.zoom_scale

        xdata, ydata = self.ax.transData.inverted().transform((event.x, event.y))
        self.ax.set_xlim([xdata - (xdata - self.ax.get_xlim()[0]) / scale_factor,
                          xdata + (self.ax.get_xlim()[1] - xdata) / scale_factor])
        self.ax.set_ylim([ydata - (ydata - self.ax.get_ylim()[0]) / scale_factor,
                          ydata + (self.ax.get_ylim()[1] - ydata) / scale_factor])
        self.canvas.draw()

    def on_click(self, event):
        self.last_click_position = (event.x, event.y)

    def on_drag(self, event):
        dx = (event.x - self.last_click_position[0]) * 1.5  # Increase panning sensitivity
        dy = (event.y - self.last_click_position[1]) * 1.5  # Increase panning sensitivity
        self.last_click_position = (event.x, event.y)

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Adjust the limits to allow panning beyond the original data bounds
        self.ax.set_xlim([xlim[0] - dx * (xlim[1] - xlim[0]) / self.plot_area.winfo_width(),
                          xlim[1] - dx * (xlim[1] - xlim[0]) / self.plot_area.winfo_width()])
        self.ax.set_ylim([ylim[0] + dy * (ylim[1] - ylim[0]) / self.plot_area.winfo_height(),
                          ylim[1] + dy * (ylim[1] - ylim[0]) / self.plot_area.winfo_height()])

        self.canvas.draw()
