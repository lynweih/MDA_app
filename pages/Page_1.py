# App Creation - Dash Board


# Import Packages 

import dash
from dash import html, dcc, callback
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas as gpd 
import matplotlib as plt
import plotly.io as pio
import plotly.graph_objects as go
import folium
from dash.dependencies import Input, Output

aed_within_provinces = gpd.read_file("App Datasets/AED_WITHIN_PROVINCES.geojson")
aed_and_popul_density_within_provinces= gpd.read_file("App Datasets/AED_DENS_POPUL_WITHIN_PROVINCES.geojson")

aed_within_provinces["cap_address"] = aed_within_provinces["address"].apply(lambda x: x.title())
# aed_within_provinces["cap_address"] = aed_within_provinces["cap_address"] + str(aed_within_provinces["number"])
aed_within_provinces["cap_address"]  = aed_within_provinces["cap_address"] + " " + aed_within_provinces["number"].astype(str)
aed_within_provinces["cap_municipality"] = aed_within_provinces["municipality"].apply(lambda x: x.title())

aed_within_provinces["cap_province"] = aed_within_provinces["province_right"].apply(lambda x: x.title())



labels ={"cap_province":"Province Name", "lat":"Latitude", "lng": "Longitude",
        "cap_address":"Address", "cap_municipality":"Municipality"}
hover_data = {"cap_province":True, "cap_address":False, "lat":False, "lng":False, "cap_municipality":True}

bel_fig = px.scatter_mapbox(aed_within_provinces, lat="lat", lon="lng", color="cap_province",
                        # size = 0.8,
                #   color_continuous_scale=px.colors.sequential.matter, 
                
                size_max=40, zoom=6.7, 
                    # text="cap_province", 
                    opacity = 1,
                    labels=labels, 
                    # title=f"AED Locations Across Provinces", 
                    hover_name="cap_address",
                    hover_data=hover_data,
                mapbox_style="carto-positron")


aed_and_popul_density_within_provinces["new_province"] = aed_and_popul_density_within_provinces["province"].apply(lambda x: x.capitalize())

df = px.data.election()
geo_df = gpd.GeoDataFrame.from_features(
    px.data.election_geojson()["features"]
).merge(df, on="district").set_index("district")

bel_fig_2 = px.choropleth_mapbox(aed_and_popul_density_within_provinces,
                           geojson=aed_and_popul_density_within_provinces.geometry,
                           locations=aed_and_popul_density_within_provinces.index,
                           hover_name="new_province",
                           color="AED_number",
                           center={"lat":50.836032848225344 , "lon": 4.3706868102113186},
                           mapbox_style="open-street-map",
                        #    title = "Number of AED in Absolute Numbers",
                           color_continuous_scale = "RdBu",
                           zoom=5.8)

bel_fig_3= px.choropleth_mapbox(aed_and_popul_density_within_provinces,
                           geojson=aed_and_popul_density_within_provinces.geometry,
                           locations=aed_and_popul_density_within_provinces.index,
                           hover_name="new_province",
                           color="AED_per_thousand",
                           center={"lat":50.836032848225344 , "lon": 4.3706868102113186},
                           mapbox_style="open-street-map",
                        #    title = "Number of AED per 1000 People Province",
                           color_continuous_scale = "RdBu",
                           zoom=5.8)





dash.register_page(__name__, path='/',name="Exploration of AED Locations")
# app = dash.Dash(__name__,use_pages=True)


layout = html.Div([
  html.H1('AED Locations in Belgium', style={'text-align':'center'}),
  html.Br(),
  html.Div([
        html.H2('AED Locations Across Provinces'),
        dcc.Graph(figure=bel_fig, style={'width': '1400px', 'height':'400px','border':'1px solid black'}),
        html.H2("AED Number per Squared Km"),
        html.Iframe(srcDoc=open(r'App Datasets/cholorpleth_provinces.html', 'r').read(), 
                    style={'width': '1200px', 'height':'400px'})
    ],style={'text-align':'center', 'font-size':22,'align-items': 'center','flex-direction': 'column','display': 'flex'}),
  html.Br(),
  html.Br(),
  html.Div([
    html.Div([
        html.H2('AED Number in Absolute Numbers'),
        dcc.Graph(figure=bel_fig_2, style={'display': 'inline-block','margin-right':'20px','border':'1px solid black'})
    ]),
    html.Div([
        html.H2('AED Number Per Thousand People'),
        dcc.Graph(figure=bel_fig_3, style={'display': 'inline-block', 'margin-left':'20px','border':'1px solid black'})
    ])
], style={'display': 'flex', 'justify-content': 'center'}),

  html.H1("AED Locations of a Specific Province"), 
  html.Div(
    children=[
    html.Div(
        children=[
        html.H2('Select Province'),
        html.Br(),
        # Add a dropdown with identifier
        dcc.Dropdown(id='province_select',
        # Set the available options with noted labels and values
        options=[
            {'label':'Antwerpen', 'value':'antwerpen'},
            {'label':'Oost-Vlaanderen', 'value':'oost-vlaanderen'},
            {'label':'Vlaams-Brabant', 'value':'vlaams-brabant'},
            {'label':'Limburg', 'value':'limburg'},
            {'label':'West-Vlaanderen', 'value':'west-vlaanderen'},
            {'label':'Henegouwen', 'value':'hainaut'},
            {'label':'Luik', 'value':'liège'},
            {'label':'Luxemburg', 'value':'luxembourg'},
            {'label':'Namen', 'value':'namur'},
            {'label':'Waals-Brabant', 'value':'brabant wallon'},
            {'label':'Brussels', 'value':'bruxelles-brussel'}],
            style={'width':'200px', 'margin':'0 auto'})
        ],
        style={'width':'250px','border':'1px solid black', 'display':'inline-block','vertical-align':'top','margin-right':'20px','padding-bottom':'100px'}),
    html.Div(children=[
            # Add a graph component with identifier
            dcc.Graph(id='major_cat')
            ],
             style={'width':'1000px','border':'1px solid black','display':'inline-block','vertical-align':'top','margin':'0px 0px 50px 70px'}
             ),
    ],style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'})], 
  style={'text-align':'center','background-color':'rgb(224, 255, 252)'}
  )

@callback(
    # Set the input and output of the callback to link the dropdown to the graph
    Output(component_id='major_cat', component_property='figure'),
    Input(component_id='province_select', component_property='value')
)

def update_plot(input_country):
    minor_cat_title = 'antwerpen'
    ecom_line = aed_within_provinces.copy(deep=True)

    labels = {"cap_province": "Province Name", "lat": "Latitude", "lng": "Longitude",
              "cap_address": "Address", "cap_municipality": "Municipality"}
    hover_data = {"cap_province": True, "cap_address": False, "lat": False, "lng": False, "cap_municipality": True}

    fig = px.scatter_mapbox(ecom_line[ecom_line["province_right"]==minor_cat_title], lat="lat", lon="lng", 
                        # color=color_series,
                #   color_continuous_scale=px.colors.sequential.matter, 
                    size_max=40, zoom=10, 
                        # text="cap_province", 
                        # color ="red",
                        opacity = 1,
                    labels=labels, 
                    title=f"{minor_cat_title.capitalize()} - Belgium", 
                    hover_name="cap_address",
                    hover_data=hover_data,
                    mapbox_style="carto-positron")  # Initialize with a default empty figure
    
    if input_country:
        minor_cat_title = input_country

        fig = px.scatter_mapbox(ecom_line[ecom_line["province_right"]==minor_cat_title], lat="lat", lon="lng", 
                        # color=color_series,
                #   color_continuous_scale=px.colors.sequential.matter, 
                    size_max=40, zoom=10, 
                        # text="cap_province", 
                        # color ="red",
                        opacity = 1,
                    labels=labels, 
                    title=f"{minor_cat_title.capitalize()} - Belgium", 
                    hover_name="cap_address",
                    hover_data=hover_data,
                    mapbox_style="carto-positron")
    
    return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)



