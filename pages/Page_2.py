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

#########################################################################################################################################################

cardiac = pd.read_csv(r"App Datasets/cardiac.csv",index_col=False)

# Your Mapbox access token
mapbox_access_token = ''

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



dash.register_page(__name__,name="Clustering and Emergency Vectors Distribution")
 
layout = html.Div([
    html.H1('Cardiac Arrests in Relation to AEDs', style={'text-align': 'center'}),
    html.Br(),
    html.Div([
        dcc.Graph(figure=fig_cluster, style={'width':'1400px','height':'600px'}),
        html.H1('Vectors Distribution in Provinces', style={'text-align': 'center'}),
        html.Iframe(srcDoc=open(r'App Datasets/Cholorpleth_Counts_Municipalities.html', 'r').read(), 
                    style={'width': '1200px', 'height':'500px',"margin-bottom":"40px"})
    ],style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
], style={'text-align':'center','align-items': 'center','background-color':'rgb(224, 255, 252)'})

   









