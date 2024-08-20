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
import dash_table
from dash_table import DataTable, FormatTemplate

area_provinces = gpd.read_file("App Datasets/AREA_PROVINCES_NEW.geojson") 

aed_per_municipality_ant = pd.read_csv(r"App Datasets/AED_per_municipality_antwerpen.csv", index_col=False)
aed_per_municipality_brx = pd.read_csv(r"App Datasets/AED_per_municipality_bruxelles-brussel.csv", index_col=False)
aed_per_municipality_liege = pd.read_csv(r"App Datasets/AED_per_municipality_liège.csv", index_col=False)
aed_per_municipality_namur = pd.read_csv(r"App Datasets/AED_per_municipality_namur.csv", index_col=False)
aed_per_municipality_hainaut = pd.read_csv(r"App Datasets/AED_per_municipality_hainaut.csv", index_col=False)
aed_per_municipality_limburg = pd.read_csv(r"App Datasets/AED_per_municipality_limburg.csv", index_col=False)
aed_per_municipality_luxembourg = pd.read_csv(r"App Datasets/AED_per_municipality_luxembourg.csv", index_col=False)
aed_per_municipality_vlaams_braband = pd.read_csv(r"App Datasets/AED_per_municipality_vlaams-brabant.csv", index_col=False)
aed_per_municipality_west_flanders = pd.read_csv(r"App Datasets/AED_per_municipality_west-vlaanderen.csv", index_col=False)
aed_per_municipality_oost_flanders = pd.read_csv(r"App Datasets/AED_per_municipality_oost-vlaanderen.csv", index_col=False)
aed_per_municipality_brabant_wallon = pd.read_csv(r"App Datasets/AED_per_municipality_brabant wallon.csv", index_col=False)

cardiac_municipality_anterpen = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_antwerpen.csv", index_col=False)
cardiac_municipality_brabant_wall = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_brabant_wall.csv", index_col=False)
cardiac_municipality_hainaut = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_hainaut.csv", index_col=False)
cardiac_municipality_liege = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_liege.csv", index_col=False)
cardiac_municipality_limburg = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_limburg.csv", index_col=False)
cardiac_municipality_namur = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_namur.csv", index_col=False)
cardiac_municipality_luxem = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_luxem.csv", index_col=False)
cardiac_municipality_west_vlaand = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_west_vlaand.csv", index_col=False)
cardiac_municipality_oost_vlaand = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_oost_vlaand.csv", index_col=False)
cardiac_municipality_vlaams_braband = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_vlaams_brabant.csv", index_col=False)
cardiac_municipality_brussels = pd.read_csv(r"App Datasets/CARDIAC_per_municipality_brussels.csv", index_col=False)

# list_cardiac_municipality = [cardiac_municipality_anterpen, cardiac_municipality_brabant_wall, cardiac_municipality_hainaut, cardiac_municipality_liege,
#                              cardiac_municipality_limburg,cardiac_municipality_namur,cardiac_municipality_luxem,cardiac_municipality_west_vlaand,
#                              cardiac_municipality_oost_vlaand,cardiac_municipality_vlaams_braband,cardiac_municipality_brussels]

def lat_split(text):
    lat = float(text.split(',')[1].strip('()'))
    return lat

def lng_split(text):
    lat = float(text.split(',')[0].strip('()'))
    return lat

list_aed_municipality = [aed_per_municipality_ant,aed_per_municipality_brabant_wallon,aed_per_municipality_hainaut,
                         aed_per_municipality_liege,aed_per_municipality_limburg,aed_per_municipality_namur,
                         aed_per_municipality_luxembourg,aed_per_municipality_west_flanders, aed_per_municipality_oost_flanders,
                         aed_per_municipality_vlaams_braband,aed_per_municipality_brx]


list_cardiac_municipality = [cardiac_municipality_anterpen, cardiac_municipality_brabant_wall, cardiac_municipality_hainaut, cardiac_municipality_liege,
                             cardiac_municipality_limburg,cardiac_municipality_namur,cardiac_municipality_luxem,cardiac_municipality_west_vlaand,
                             cardiac_municipality_oost_vlaand,cardiac_municipality_vlaams_braband,cardiac_municipality_brussels]


list_province_name =['antwerpen','brabant wallon','hainaut', 'liège','limburg','namur'
                     ,'luxembourg','west-vlaanderen','oost-vlaanderen','vlaams-brabant','bruxelles-brussel']

list_aed_cardiac_name = list(zip(list_aed_municipality,list_cardiac_municipality,list_province_name))

def bubble_across_be(aed_df, cardiac_df, province_name):
    
   aed_cardiac_per_municipality_ant = cardiac_df.merge(aed_df, on="points_coordinates")
   aed_cardiac_per_municipality_ant["lat"] = aed_cardiac_per_municipality_ant["points_coordinates"].apply(lat_split)
   aed_cardiac_per_municipality_ant["lng"] = aed_cardiac_per_municipality_ant["points_coordinates"].apply(lng_split)
   aed_cardiac_per_municipality_ant['geometry'] = gpd.points_from_xy(aed_cardiac_per_municipality_ant["lng"], aed_cardiac_per_municipality_ant["lat"])
   aed_cardiac_per_municipality_ant_geo = gpd.GeoDataFrame(aed_cardiac_per_municipality_ant, 
                           crs = area_provinces.crs, 
                           geometry = aed_cardiac_per_municipality_ant["geometry"])
   province_co = area_provinces.loc[area_provinces['province'] == province_name]
   aed_cardiac_per_municipality_ant_geo_merged = gpd.sjoin(aed_cardiac_per_municipality_ant_geo, province_co, predicate = 'within')
   aed_cardiac_per_municipality_ant_geo_merged["cardiac_to_aed"] = aed_cardiac_per_municipality_ant_geo_merged["cardiac_arrests_number"] / aed_cardiac_per_municipality_ant_geo_merged["AED_number"]
   aed_cardiac_per_municipality_ant_geo_merged["municipality_name"] = aed_cardiac_per_municipality_ant_geo_merged["new_municipality_x"].apply(lambda x: x.split()[0].strip(",").capitalize())

   return aed_cardiac_per_municipality_ant_geo_merged  

aed_cardiac_to_combine = []

for i, name in enumerate(list_aed_cardiac_name):
    aed_cardiac= bubble_across_be(name[0], name[1], name[2])
    aed_cardiac_to_combine.append(aed_cardiac)

    combined_df = pd.concat(aed_cardiac_to_combine, ignore_index=True)

labels ={"cardiac_to_aed":"Cardiac/AED (Ratio)","municipality_name": "Municipality", "lat":"Latitude", "lng": "Longitude", "AED_number":"AED Number"
         ,"cardiac_arrests_number":"Cardiac Arrests"}
hover_data = {"cardiac_arrests_number":True, "AED_number":True, "lat":False, "lng":False}

fig_bubble_bel = px.scatter_mapbox(combined_df, lat="lat", lon="lng", color="cardiac_to_aed", size="AED_number",
                  color_continuous_scale=px.colors.sequential.matter, size_max=80, zoom=10, text="municipality_name", labels=labels, 
                  title=f"AED and Cardiac Arrests Distribution Per Municipality - Belgium", opacity=0.8, 
                   hover_name="municipality_name",
                   hover_data=hover_data,
                  mapbox_style="carto-positron")



# fig.show()
def plot_bubble(aed_df, cardiac_df, province_name):

   aed_cardiac_per_municipality_ant = cardiac_df.merge(aed_df, on="points_coordinates")
   aed_cardiac_per_municipality_ant["lat"] = aed_cardiac_per_municipality_ant["points_coordinates"].apply(lat_split)
   aed_cardiac_per_municipality_ant["lng"] = aed_cardiac_per_municipality_ant["points_coordinates"].apply(lng_split)
   aed_cardiac_per_municipality_ant['geometry'] = gpd.points_from_xy(aed_cardiac_per_municipality_ant["lng"], aed_cardiac_per_municipality_ant["lat"])
   aed_cardiac_per_municipality_ant_geo = gpd.GeoDataFrame(aed_cardiac_per_municipality_ant, 
                           crs = area_provinces.crs, 
                           geometry = aed_cardiac_per_municipality_ant["geometry"])
   province_co = area_provinces.loc[area_provinces['province'] == province_name]
   aed_cardiac_per_municipality_ant_geo_merged = gpd.sjoin(aed_cardiac_per_municipality_ant_geo, province_co, predicate = 'within')
   aed_cardiac_per_municipality_ant_geo_merged["cardiac_to_aed"] = aed_cardiac_per_municipality_ant_geo_merged["cardiac_arrests_number"] / aed_cardiac_per_municipality_ant_geo_merged["AED_number"]
   aed_cardiac_per_municipality_ant_geo_merged["municipality_name"] = aed_cardiac_per_municipality_ant_geo_merged["new_municipality_x"].apply(lambda x: x.split()[0].strip(",").capitalize())

   labels ={"cardiac_to_aed":"Cardiac/AED (Ratio)","municipality_name": "Municipality", "lat":"Latitude", "lng": "Longitude", "AED_number":"AED Number"
         ,"cardiac_arrests_number":"Cardiac Arrests"}
   hover_data = {"cardiac_arrests_number":True, "AED_number":True, "lat":False, "lng":False}


   fig = px.scatter_mapbox(aed_cardiac_per_municipality_ant_geo_merged, lat="lat", lon="lng", color="cardiac_to_aed", size="AED_number",
                  color_continuous_scale=px.colors.sequential.matter, size_max=80, zoom=10, text="municipality_name", labels=labels, 
                  title=f"AED and Cardiac Arrests Distribution Per Municipality - {province_name.capitalize()}", opacity=0.8, 
                   hover_name="municipality_name",
                   hover_data=hover_data,
                  mapbox_style="carto-positron")
   return (fig, aed_cardiac_per_municipality_ant_geo_merged[["municipality_name","cardiac_arrests_number","AED_number","cardiac_to_aed"]])

antwerp_bubble, ant_dataset = plot_bubble(aed_per_municipality_ant, cardiac_municipality_anterpen, 'antwerpen')
brabant_wallon_bubble, brabant_dataset = plot_bubble(aed_per_municipality_brabant_wallon, cardiac_municipality_brabant_wall,'brabant wallon')
hainaut_bubble, hainaut_dataset = plot_bubble(aed_per_municipality_hainaut, cardiac_municipality_hainaut, 'hainaut')
liege_bubble, liege_dataset = plot_bubble(aed_per_municipality_liege, cardiac_municipality_liege, 'liège')
limburg_bubble, limburg_dataset = plot_bubble(aed_per_municipality_limburg, cardiac_municipality_limburg, 'limburg')
namur_bubble, namur_dataset = plot_bubble(aed_per_municipality_namur, cardiac_municipality_namur, 'namur')
luxembourg_bubble, luxem_dataset = plot_bubble(aed_per_municipality_luxembourg, cardiac_municipality_luxem, 'luxembourg')
west_vlaanderen_bubble, west_dataset = plot_bubble(aed_per_municipality_west_flanders, cardiac_municipality_west_vlaand, 'west-vlaanderen')
oost_vlaanderen_bubble, oost_dataset = plot_bubble(aed_per_municipality_oost_flanders, cardiac_municipality_oost_vlaand, 'oost-vlaanderen')
vlaams_brabant_bubble, vlaams_dataset = plot_bubble(aed_per_municipality_vlaams_braband, cardiac_municipality_vlaams_braband, 'vlaams-brabant')
brussel_bubble, brussel_dataset = plot_bubble(aed_per_municipality_brx, cardiac_municipality_brussels, 'bruxelles-brussel')



################################################

bubble_bel_dataframe = combined_df[["municipality_name","cardiac_arrests_number","AED_number","cardiac_to_aed"]]

# d_columns = [{'name':x, 'id':x} for x in bubble_bel_dataframe.columns]

d_columns = [{'name':'Municipality', 'id':'municipality_name'},
             {'name':'Cardiac Arrests', 'id':'cardiac_arrests_number'},
             {'name':'AED Number', 'id':'AED_number'},
             {'name':'Cardiac / AED','id':'cardiac_to_aed'}]


bel_bubble_table  = DataTable(
  			# Set up the columns and data
            columns=d_columns,
            data=bubble_bel_dataframe.to_dict('records'),
            cell_selectable=False,
  			# Set up sort, filter and pagination
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_current= 0,
            page_size= 10,
            )


def bubble_table(province_dataset):
    province_table = DataTable(
  			# Set up the columns and data
            columns=d_columns,
            data=province_dataset.to_dict('records'),
            cell_selectable=False,
  			# Set up sort, filter and pagination
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_current= 0,
            page_size= 10,
            )
    return province_table

#################################################################################################################################################################

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


 





dash.register_page(__name__,name="Analysis of Cardiac Arrests")

layout = html.Div([
    html.H1('Cardiac Arrests in Relation to AEDs', style={'text-align': 'center'}),
    html.H2('Municipality Level', style={'text-align': 'center'}),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig_bubble_bel, style={'width': '1400px', 'height':'700px', 'margin-bottom':'40px'})
        ], style={}),
        html.Br(),
        html.Div([
            bel_bubble_table
        ], style={'width':'800px'})
    ], style={"text-align":'center','align-items': 'center','flex-direction': 'column','display': 'flex'}),
    html.Br(),
    html.Br(),
    html.H2("Cardiac Arrests Distribution Across Municipalities for Specific Province"),
    html.Div([
            html.H3("Select A Province"),
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
                style={'width': '200px', 'display': 'inline-block'})
            ], style={'width': '400px', 'border': '2px solid red', 'text-align': 'center', 'margin': '0 auto'}),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id='bubble_plot',style={'width': '1400px', 'height':'700px', 'margin-bottom':'40px'})]),
        html.Div([
            dash_table.DataTable(
            id='table',
            columns=d_columns,
            data=[],  # Data will be set dynamically
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action='native',
            page_current=0,
            page_size=10,
        )],style={'width':'800px'})
        
    ],style={"text-align":'center','align-items': 'center','flex-direction': 'column','display': 'flex'}),
    html.Br(),
    html.Div([
        html.H1("Ratio of (Cardiac Arrest Number / AMB+PIT+MUG+AED+1)"),
        html.Iframe(srcDoc=open(r"App Datasets/Cholorpleth_Cardiac_Arrests_Municipalities.html", 'r').read(), 
                    style={'width': '1200px', 'height':'500px',"margin-bottom":"40px"})
    ])
],style={'text-align':'center','background-color':'rgb(224, 255, 252)'})
        
@callback(
    # Set the input and output of the callback to link the dropdown to the graph
    
    Output(component_id='bubble_plot', component_property='figure'),
    Output(component_id="table", component_property='data'),
    Input(component_id='province_select', component_property='value')
)

def update_plot(input_province):
    bubble, dataset = plot_bubble(aed_per_municipality_ant, cardiac_municipality_anterpen, 'antwerpen')
    if input_province:
        if input_province == 'brabant wallon':
            bubble, dataset = plot_bubble(aed_per_municipality_brabant_wallon, cardiac_municipality_brabant_wall,'brabant wallon')
        elif input_province == 'hainaut':
            bubble, dataset = plot_bubble(aed_per_municipality_hainaut, cardiac_municipality_hainaut, 'hainaut')
        elif input_province == "liège":
            bubble, dataset = plot_bubble(aed_per_municipality_liege, cardiac_municipality_liege, 'liège')
        elif input_province == "limburg":
            bubble, dataset = plot_bubble(aed_per_municipality_limburg, cardiac_municipality_limburg, 'limburg')
        elif input_province == "namur":
            bubble, dataset = plot_bubble(aed_per_municipality_namur, cardiac_municipality_namur, 'namur')
        elif input_province == "luxembourg":
            bubble, dataset = plot_bubble(aed_per_municipality_luxembourg, cardiac_municipality_luxem, 'luxembourg')
        elif input_province == "west-vlaanderen":
            bubble, dataset = plot_bubble(aed_per_municipality_west_flanders, cardiac_municipality_west_vlaand, 'west-vlaanderen')
        elif input_province == 'oost-vlaanderen':
            bubble, dataset = plot_bubble(aed_per_municipality_oost_flanders, cardiac_municipality_oost_vlaand, 'oost-vlaanderen')
        elif input_province == 'vlaams-brabant':
            bubble, dataset = plot_bubble(aed_per_municipality_vlaams_braband, cardiac_municipality_vlaams_braband, 'vlaams-brabant')
        elif input_province == 'antwerpen':
            bubble, dataset = plot_bubble(aed_per_municipality_ant, cardiac_municipality_anterpen, 'antwerpen')
        else:
            bubble, dataset = plot_bubble(aed_per_municipality_brx, cardiac_municipality_brussels, 'bruxelles-brussel')

    return bubble, dataset.to_dict('records')

            
        



    
    

