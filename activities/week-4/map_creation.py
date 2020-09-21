 
import folium
import pandas as pd
import geopandas as gpd
from folium.plugins import FloatImage
from branca.element import Template, MacroElement

legend_abrev = {
    "Vegetables": "V",
    "Fruits": "F",
    "Grains/Legumes/Nuts/Seeds": "G/L/N/S",
    "Meat/Poultry": "M",
    "Fish/Seafood": "F/S",
    "Dairy Food Group": "D",
    "Eggs": "E",
    "Sugar": "S"
}


def generate_legend_html(df_cluster_centroid, colors):  
    legend_html = ""
    for row_dict, color in zip(df_cluster_centroid.round(2).to_dict('records'), colors):
        row_dict = {legend_abrev[key]: value for key, value in row_dict.items()}
        legend_html += f"<li><span style='background:{color};opacity:0.7;'></span>{str(row_dict)}</li>"
        
    return legend_html

def generate_food_group_map(df_cluster_labels, legend):
    country_geojson = "datasets/countries.geojson"
    df_geo = gpd.read_file(country_geojson)
    
    m = folium.Map(zoom_start=50, max_bounds=True)

    folium.Choropleth(
        geo_data=df_geo,
        bins=6,
        name='Food groups',
        data=df_cluster_labels,
        columns=['ISO_A2', 'Group'],
        key_on='feature.properties.ISO_A2',
        fill_color='RdYlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Food groups',
    ).add_to(m)


    with open("folium_legend_template", "r") as f:
        template = f.read().replace('\n', '')
        template = template.replace("{legend_clusters}", legend)

    macro = MacroElement()
    macro._template = Template(template)
    m.get_root().add_child(macro)
    
    return m
