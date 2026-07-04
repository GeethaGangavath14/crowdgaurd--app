# utils/map_generator.py
import folium
from folium.plugins import HeatMap

def generate_heatmap(locations):
    m = folium.Map(location=[17.4065, 78.4772], zoom_start=16)
    HeatMap(locations).add_to(m)
    m.save("templates/heatmap.html")
