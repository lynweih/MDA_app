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
from geopy.distance import geodesic


cardiac = pd.read_csv(r"App/App Datasets/cardiac.csv",index_col=False)

# Your Mapbox access token
mapbox_access_token = 'pk.eyJ1Ijoid2VuaGFuY3UiLCJhIjoiY2x3cTlrYjlnMDAybTJqczdzOWFwcWpjdyJ9.yNEGbGM7vNhqbdfdfFNTng'

labels={"cluster":"Cardiac Arrest Level"}
# Create the map
fig_cluster = px.scatter_mapbox(cardiac, lat='latitude intervention', lon='longitude intervention',
                        color='cluster',
                        center=dict(lat=50.8503, lon=4.3517), 
                        zoom=7, 
                        mapbox_style="open-street-map",
                        title="Clustered Municipalities Based on Cardiac Arrests",
                        labels=labels)  # Use an appropriate Mapbox style

# Update the layout with your Mapbox token
fig_cluster.update_layout(mapbox=dict(accesstoken=mapbox_access_token))

# Show the figure
# fig.show()

##################################################################################################################################################################

vecotrs = gpd.read_file("App/App Datasets/Vecotrs.geojson")
cardiac_location = gpd.read_file("App/App Datasets/Cardiac_location.geojson")
aed = gpd.read_file(r"App/App Datasets/AED_GEO.geojson")
aed = aed.to_crs(epsg=4326)
aed = aed[['lat', 'lng']]

# Your Mapbox access token
mapbox_access_token = 'pk.eyJ1Ijoid2VuaGFuY3UiLCJhIjoiY2x3cTlrYjlnMDAybTJqczdzOWFwcWpjdyJ9.yNEGbGM7vNhqbdfdfFNTng'


# Create initial figure
fig_optim = px.scatter_mapbox(cardiac_location, lat='lat', lon='lng',
                        center=dict(lat=50.8503, lon=4.3517),
                        zoom=7, mapbox_style="open-street-map")

fig_optim.update_layout(mapbox=dict(accesstoken=mapbox_access_token))

# Helper function to find the nearest point
def find_nearest_point(lat, lng, df):
    distances = df.apply(lambda row: geodesic((lat, lng), (row['lat'], row['lng'])).meters, axis=1)
    nearest_index = distances.idxmin()
    return df.loc[nearest_index, 'lat'], df.loc[nearest_index, 'lng']




##############################################################################################################################################################


dash.register_page(__name__,name="Proximity of AED & Ambulance")

layout = html.Div([
    html.H1("Nearest Location of AED and Emergency Vector Given A Heart Related Incident"),
    html.Br(),
    html.H2("Choose an Emergency Incident on the Map to Obtain the Nearest AED and Ambulance", style={'border': '2px solid red'}),
    html.Br(),
    html.H3("Blue Dots: Heart Related Emergency",style={'text-align': 'left'}),
    html.Div([
            dcc.Graph(id='map', figure=fig_optim, config={'scrollZoom': True},style={'height':"800px"}),
            dcc.Store(id='pin-location')])

], style={'text-align':'center','background-color':'rgb(224, 255, 252)'})


# Callback to handle pin drop
@callback(
    Output('map', 'figure'),
    [Input('map', 'clickData')],
    prevent_initial_call=True
)

def update_map(clickData):
    if clickData is None:
        return dash.no_update

    lat = clickData['points'][0]['lat']
    lng = clickData['points'][0]['lon']

    # Find nearest AED
    nearest_aed_lat, nearest_aed_lng = find_nearest_point(lat, lng, aed)

    # Find nearest ambulance
    nearest_ambulance_lat, nearest_ambulance_lng = find_nearest_point(lat, lng, vecotrs)

    # Create the figure
    fig = px.scatter_mapbox(cardiac_location, lat='lat', lon='lng',
                            center=dict(lat=50.8503, lon=4.3517),
                            zoom=7, mapbox_style="open-street-map")
    fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token))

    # Add the pin location
    fig.add_trace(go.Scattermapbox(
        lat=[lat],
        lon=[lng],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14, color='red'),
        name='Emergency Incident Location'
    ))

    # Add the nearest AED location
    fig.add_trace(go.Scattermapbox(
        lat=[nearest_aed_lat],
        lon=[nearest_aed_lng],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14, color='green'),
        name='Nearest AED'
    ))

    # Add the nearest ambulance location
    fig.add_trace(go.Scattermapbox(
        lat=[nearest_ambulance_lat],
        lon=[nearest_ambulance_lng],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14, color='blue'),
        name='Nearest Ambulance'
    ))

    # Add lines connecting the pin to the nearest AED and ambulance
    fig.add_trace(go.Scattermapbox(
        lat=[lat, nearest_aed_lat],
        lon=[lng, nearest_aed_lng],
        mode='lines',
        line=dict(width=2, color='green'),
        name='Line to Nearest AED'
    ))

    fig.add_trace(go.Scattermapbox(
        lat=[lat, nearest_ambulance_lat],
        lon=[lng, nearest_ambulance_lng],
        mode='lines',
        line=dict(width=2, color='blue'),
        name='Line to Nearest Emergency Vector'
    ))

    return fig

