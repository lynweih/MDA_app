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

# ######################################################## Map and Bar Plot Probability Risk ######################################################

################################# Map 

area_provinces = gpd.read_file("App Datasets/AREA_PROVINCES_NEW.geojson") 

interventions_risk = pd.read_csv(r"App Datasets/Interventions_risky_probability.csv", index_col=False)

percentile_75 = interventions_risk['Intervention duration'].quantile(0.75)

# provinces_risk = interventions_risk.groupby("Province intervention")["Probability_Risk"].mean().to_frame().reset_index()
provinces_risk = interventions_risk.groupby("Province intervention")[["Probability_Risk", "Calculated Distance destination",
                                                                      "distance_to_intervention","Intervention duration"]].mean().reset_index()

provinces_risk= provinces_risk.rename(columns={'Province intervention': 'province'})

old_to_new_name = {"ANT":"antwerpen","BRW":"brabant wallon","BXL":"bruxelles-brussel","HAI":"hainaut","LIE":"liège","LIM":"limburg","LUX":"luxembourg","NAM":"namur"}
provinces_risk['province'] = provinces_risk['province'].replace(old_to_new_name)

area_provinces_risk = area_provinces.merge(provinces_risk, on="province",how="left")

def convert_str_tuple(text):
    lat = float(text.split(",")[0].strip('('))
    long = float(text.split(",")[1].strip().strip(')'))
    return (lat,long)

# area_provinces_risk["center"] = area_provinces_risk["center"].apply(convert_str_tuple)

# brussels_center = area_provinces_risk["center"][1]

area_provinces_risk["province_cap"] = area_provinces_risk["province"].apply(lambda x: x.capitalize())
                
df = px.data.election()
geo_df = gpd.GeoDataFrame.from_features(
    px.data.election_geojson()["features"]
).merge(df, on="district").set_index("district")

labels = {"Probability_Risk":"Average Predicted Probability"}
# hover_data = {"area_provinces_risk.index":False}

fig_risk_map = px.choropleth_mapbox(area_provinces_risk,
                           geojson=area_provinces_risk.geometry,
                           locations=area_provinces_risk.index,
                           hover_name = "province_cap",
                           color="Probability_Risk",
                           center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                           mapbox_style="carto-positron",
                           title="Average Predicted Probability of Intervention Duration Above 68 Minutes (75th Percentile)",
                           labels=labels,
                        #    hover_data = hover_data,
                           zoom=6.5)
# fig.show()

###################### Bar Plot

area_provinces_risk = area_provinces.merge(provinces_risk, on="province")
area_provinces_risk["province_cap"] = area_provinces_risk["province"].apply(lambda x: x.capitalize())

fig_bar = go.Figure(
    data=go.Bar(
        x=area_provinces_risk["province_cap"],
        y=area_provinces_risk["Calculated Distance destination"],
        name="Provinces",
        marker=dict(color="paleturquoise"),

    )
)

fig_bar.add_trace(
    go.Bar(
        x=area_provinces_risk["province_cap"],
        y=area_provinces_risk["Probability_Risk"],
        name="Probability_Risk",
        marker=dict(color="crimson"),
    )
)


fig_bar.add_trace(
    go.Scatter(
        x=area_provinces_risk["province_cap"],
        y=area_provinces_risk["Probability_Risk"],
        yaxis="y2",
        name="Probability",
        marker=dict(color="crimson"),
    )
)
# fig_bar.add_trace(
#     go.Scatter(
#         x=area_provinces_risk["province_cap"],
#         y=area_provinces_risk["Intervention duration"],
#         yaxis="y2",
#         name="Probability",
#         marker=dict(color="crimson"),
#     )
# )



fig_bar.update_layout(
    title="Average Distance to Hospital (All Vector Types) vs Average Predicted Probality of Intervention Delay",
    # title="Distance to Hospital vs Average Intervention Duration",
    legend=dict(orientation="h"),
    yaxis=dict(
        title=dict(text="Distance to Hospital (Meters)"),
        side="left",
        range=[0, 17000],
    ),
    yaxis2=dict(
        title=dict(text="Avg. Predicted Probabity of Delay"),
        side="right",
        range=[0.1, 0.45],
        overlaying="y",
        tickmode="sync",
    ),
#    yaxis2=dict(
#         title=dict(text="Avg. Predicted Probabity of Delay"),
#         side="right",
#         range=[50, 70],
#         overlaying="y",
#         tickmode="sync",
#     ),
)

# fig.show()


# fig.show()

# ################################################################################################################################################################

# ######################################################### Map Intervention Duration and Line Plot ###############################################################

interventions_risk_grouped = interventions_risk.groupby(["Province intervention","time_period"])["Intervention duration"].mean().to_frame().reset_index()

interventions_risk_grouped = interventions_risk_grouped.pivot(index='Province intervention', columns='time_period', values='Intervention duration')

interventions_risk_grouped.reset_index()
interventions_risk_grouped.columns.name = None

interventions_risk_grouped = interventions_risk_grouped.reset_index()

interventions_risk_grouped= interventions_risk_grouped.rename(columns={'Province intervention': 'province'})
old_to_new_name = {"ANT":"antwerpen","BRW":"brabant wallon","BXL":"bruxelles-brussel","HAI":"hainaut","LIE":"liège","LIM":"limburg","LUX":"luxembourg","NAM":"namur"}
interventions_risk_grouped['province'] = interventions_risk_grouped['province'].replace(old_to_new_name)

# interventions_risk_grouped

area_provinces_risk_new = area_provinces_risk.merge(interventions_risk_grouped, on="province")

df = px.data.election()
geo_df = gpd.GeoDataFrame.from_features(
    px.data.election_geojson()["features"]
).merge(df, on="district").set_index("district")

labels = {"morning":"Early Morning {08.00-10.00}", "noon":"Morning {10.00-13.00}",
          "afternoon":"Afternoon {13.00-16.00}","evening":"Evening {16.00-19.00}",
          "night":"Night {19.00-23.00}","midnight":"Midnight-Dawn{23.00-08.00}"}
# hover_data = {"area_provinces_risk.index":False}

fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                           geojson=area_provinces_risk_new.geometry,
                           locations=area_provinces_risk_new.index,
                           hover_name = "province_cap",
                           color="morning",
                           center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                           mapbox_style="carto-positron",
                           title="Average Intervention Duration",
                           labels=labels,
                        #    hover_data = hover_data,
                           zoom=6.5)
# fig.show()

############################### LINE

interventions_risk_line = interventions_risk.groupby(["Province intervention","time_period"])["Intervention duration"].mean().to_frame().reset_index()
old_to_new_name = {"ANT":"Antwerpen","BRW":"Brabant Wallon","BXL":"Bruxelles-Brussel","HAI":"Hainaut","LIE":"Liège","LIM":"Limburg","LUX":"Luxembourg","NAM":"Namur"}
interventions_risk_line['Province intervention'] = interventions_risk_line['Province intervention'].replace(old_to_new_name)


order = ['morning', 'noon', 'afternoon', 'evening', 'night', 'midnight']
interventions_risk_line['time_period'] = pd.Categorical(interventions_risk_line['time_period'], categories=order, ordered=True)
interventions_risk_line = interventions_risk_line.sort_values(['Province intervention', 'time_period']).reset_index(drop=True)
interventions_risk_line["time_period"] = interventions_risk_line["time_period"].apply(lambda x: x.capitalize())

labels = {"time_period":"Time of Day", "Province intervention":"Province Name", "Intervention duration":"Duration of Intervention"}

fig_line_interv = px.line(interventions_risk_line, x="time_period", 
              y="Intervention duration", 
              color='Province intervention', 
              labels=labels, 
              title="Duration of Intervention per Time of Day for each Province")
# fig.show()

############################# BAR

interventions_risk_line = interventions_risk.groupby(["Province intervention","time_period"])["Intervention duration"].mean().to_frame().reset_index()


new_names = {"morning":"Early Morning {08.00-10.00}", "noon":"Morning {10.00-13.00}",
          "afternoon":"Afternoon {13.00-16.00}","evening":"Evening {16.00-19.00}",
          "night":"Night {19.00-23.00}","midnight":"Midnight-Dawn {23.00-08.00}"}

def change_text(text):
    if text in new_names.keys():
        new_text = new_names[text]
    else:
        new_text = new_text
    return new_text

interventions_risk_line["time_period"] = interventions_risk_line["time_period"].apply(change_text)

old_to_new_name = {"ANT":"antwerpen","BRW":"brabant wallon","BXL":"bruxelles-brussel","HAI":"hainaut","LIE":"liège","LIM":"limburg","LUX":"luxembourg","NAM":"namur"}
interventions_risk_line['Province intervention'] = interventions_risk_line['Province intervention'].replace(old_to_new_name)
interventions_risk_line["Province intervention"] = interventions_risk_line["Province intervention"].apply(lambda x: x.capitalize())

interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Early Morning {08.00-10.00}"].reset_index(drop=True)

time_of_day = interventions_risk_line_period["time_period"][0]

labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

fig_bar_dur = px.bar(interventions_risk_line_period  , 
             x='Province intervention', 
             y='Intervention duration', 
             color="Province intervention",
             title=f"Average Intervention Duration per Province during {time_of_day}",
            labels=labels)

# fig.show()

####################################################################################################################################################################


dash.register_page(__name__,name="Intervention Duration & Predicted Probability of Delay")

layout = html.Div([
    html.H1('Intervention Duration vs Time of Day'),
    html.Div([
        html.H2('Intervention Duration Across Time Periods'),
        html.Div([
        dcc.Graph(id='intervention_map')],
        style={'width':'80%', 'height':'80%','border':'1px solid black', 'margin-bottom':'20px'}),
        html.Br(),
        html.H3('Time Period of the Day', style={'font-size': '20px'}),
        html.Div([
        dcc.Slider(0,5,step=None,
                   marks={
                          0: {'label': 'Early Morning {08.00-10.00}', 'style': {'font-size': '14px', 'font-weight': 'bold'}},
                          1: {'label': 'Morning {10.00-13.00}', 'style': {'font-size': '14px', 'font-weight': 'bold'}},
                          2: {'label': 'Afternoon {13.00-16.00}', 'style': {'font-size': '14px', 'font-weight': 'bold'}},
                          3: {'label': 'Evening {16.00-19.00}', 'style': {'font-size': '14px', 'font-weight': 'bold'}},
                          4: {'label': 'Night {19.00-23.00}', 'style': {'font-size': '14px', 'font-weight': 'bold'}},
                          5: {'label': 'Midnight-Dawn {23.00-08.00}', 'style': {'font-size': '14px', 'font-weight': 'bold'}}
                }, 
                value=3,
                          id='value_slider'
                          )], style={'width':'60%', 'height':'40%','border':'3px solid red', 'padding':'40px 70px 40px 70px'})
                          ], style={"text-align":'center','align-items': 'center','flex-direction': 'column','display': 'flex'}),
    html.Br(),
    html.Br(),
    html.Div([
            dcc.Graph(id='duration_bar', style={'display':'inline-block','border':'1px solid black','margin-right': '10px'}),
            dcc.Graph(figure=fig_line_interv, style={'display':'inline-block','border':'1px solid black','margin-left': '10px'})
            ], style={'align-items': 'center','flex-direction': 'column','display': 'inline-block'}),
    html.Br(),
    html.Div([
            html.H2('Average Predicted Probability of Vector Delay per Province'),
            dcc.Graph(figure=fig_risk_map, style={'width':'90%','border':'1px solid black','margin-bottom': '20px'}),
            dcc.Graph(figure=fig_bar, style={'width':'70%','border':'1px solid black','margin-top': '20px'})
    ],style={'display': 'flex', 
        'flex-direction': 'column', 
        'align-items': 'center', 
        'text-align': 'center'})
], style={"text-align":'center','align-items': 'center','background-color':'rgb(224, 255, 252)'})

@callback(
    Output(component_id='duration_bar', component_property='figure'),
    Output(component_id='intervention_map', component_property='figure'),
    Input(component_id='value_slider', component_property='value')
)

def update_plot(input_value):

    interventions_risk_2 = interventions_risk.copy(deep=True)

    interventions_risk_grouped = interventions_risk_2.groupby(["Province intervention","time_period"])["Intervention duration"].mean().to_frame().reset_index()

    interventions_risk_grouped = interventions_risk_grouped.pivot(index='Province intervention', columns='time_period', values='Intervention duration')

    interventions_risk_grouped.reset_index()
    interventions_risk_grouped.columns.name = None

    interventions_risk_grouped = interventions_risk_grouped.reset_index()

    interventions_risk_grouped= interventions_risk_grouped.rename(columns={'Province intervention': 'province'})
    old_to_new_name = {"ANT":"antwerpen","BRW":"brabant wallon","BXL":"bruxelles-brussel","HAI":"hainaut","LIE":"liège","LIM":"limburg","LUX":"luxembourg","NAM":"namur"}
    interventions_risk_grouped['province'] = interventions_risk_grouped['province'].replace(old_to_new_name)

    # interventions_risk_grouped

    area_provinces_risk_new = area_provinces_risk.merge(interventions_risk_grouped, on="province")

    df = px.data.election()
    geo_df = gpd.GeoDataFrame.from_features(
        px.data.election_geojson()["features"]
    ).merge(df, on="district").set_index("district")

    labels_1 = {"morning":"Early Morning {08.00-10.00}", "noon":"Morning {10.00-13.00}",
            "afternoon":"Afternoon {13.00-16.00}","evening":"Evening {16.00-19.00}",
            "night":"Night {19.00-23.00}","midnight":"Midnight-Dawn{23.00-08.00}"}
    # hover_data = {"area_provinces_risk.index":False}

    fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                            geojson=area_provinces_risk_new.geometry,
                            locations=area_provinces_risk_new.index,
                            hover_name = "province_cap",
                            color='evening',
                            center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                            mapbox_style="carto-positron",
                            title="Average Intervention Duration",
                            labels=labels_1,
                            #    hover_data = hover_data,
                            zoom=6.5)
    
    interventions_risk_line = interventions_risk_2.groupby(["Province intervention","time_period"])["Intervention duration"].mean().to_frame().reset_index()
    
    interventions_risk_line["time_period"] = interventions_risk_line["time_period"].apply(change_text) 

    interventions_risk_line['Province intervention'] = interventions_risk_line['Province intervention'].replace(old_to_new_name)
    interventions_risk_line["Province intervention"] = interventions_risk_line["Province intervention"].apply(lambda x: x.capitalize())

    interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Evening {16.00-19.00}"].reset_index(drop=True)

    

    labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

    fig_bar_dur = px.bar(interventions_risk_line_period  , 
             x='Province intervention', 
             y='Intervention duration', 
             color="Province intervention",
             title="Average Intervention Duration - Evening {16.00-19.00}",
            labels=labels)


    if input_value:

        if input_value == 0:

            fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                                geojson=area_provinces_risk_new.geometry,
                                locations=area_provinces_risk_new.index,
                                hover_name = "province_cap",
                                color='morning',
                                center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                                mapbox_style="carto-positron",
                                title="Average Intervention Duration",
                                labels=labels_1,
                                #    hover_data = hover_data,
                                zoom=6.5)
            
            interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Early Morning {08.00-10.00}"].reset_index(drop=True)

            labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

            fig_bar_dur = px.bar(interventions_risk_line_period, 
                x='Province intervention', 
                y='Intervention duration', 
                color="Province intervention",
                title="Average Intervention Duration - Early Morning {08.00-10.00}",
                labels=labels)
            
        elif input_value == 1 :

                        fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                                geojson=area_provinces_risk_new.geometry,
                                locations=area_provinces_risk_new.index,
                                hover_name = "province_cap",
                                color='noon',
                                center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                                mapbox_style="carto-positron",
                                title="Average Intervention Duration",
                                labels=labels_1,
                                #    hover_data = hover_data,
                                zoom=6.5)
                        
                        interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Morning {10.00-13.00}"].reset_index(drop=True)

                        labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

                        fig_bar_dur = px.bar(interventions_risk_line_period, 
                            x='Province intervention', 
                            y='Intervention duration', 
                            color="Province intervention",
                            title="Average Intervention Duration - Morning {10.00-13.00}",
                            labels=labels)
                        
        elif input_value == 2 :
              
                        fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                        geojson=area_provinces_risk_new.geometry,
                        locations=area_provinces_risk_new.index,
                        hover_name = "province_cap",
                        color='afternoon',
                        center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                        mapbox_style="carto-positron",
                        title="Average Intervention Duration",
                        labels=labels_1,
                        #    hover_data = hover_data,
                        zoom=6.5)

                        interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Afternoon {13.00-16.00}"].reset_index(drop=True)

                        labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

                        fig_bar_dur = px.bar(interventions_risk_line_period, 
                            x='Province intervention', 
                            y='Intervention duration', 
                            color="Province intervention",
                            title="Average Intervention Duration - Afternoon {13.00-16.00}",
                            labels=labels)





        elif input_value == 3 :
               
                        fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                        geojson=area_provinces_risk_new.geometry,
                        locations=area_provinces_risk_new.index,
                        hover_name = "province_cap",
                        color='evening',
                        center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                        mapbox_style="carto-positron",
                        title="Average Intervention Duration",
                        labels=labels_1,
                        #    hover_data = hover_data,
                        zoom=6.5)


                        interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Evening {16.00-19.00}"].reset_index(drop=True)

                        labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

                        fig_bar_dur = px.bar(interventions_risk_line_period, 
                            x='Province intervention', 
                            y='Intervention duration', 
                            color="Province intervention",
                            title="Average Intervention Duration - Evening {16.00-19.00}",
                            labels=labels)

        elif input_value == 4 :
        
                fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                geojson=area_provinces_risk_new.geometry,
                locations=area_provinces_risk_new.index,
                hover_name = "province_cap",
                color='night',
                center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                mapbox_style="carto-positron",
                title="Average Intervention Duration",
                labels=labels_1,
                #    hover_data = hover_data,
                zoom=6.5)

                
                interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Night {19.00-23.00}"].reset_index(drop=True)

                labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

                fig_bar_dur = px.bar(interventions_risk_line_period, 
                    x='Province intervention', 
                    y='Intervention duration', 
                    color="Province intervention",
                    title="Average Intervention Duration - Night {19.00-23.00}",
                    labels=labels)



        else :
              
                fig_intervention = px.choropleth_mapbox(area_provinces_risk_new,
                geojson=area_provinces_risk_new.geometry,
                locations=area_provinces_risk_new.index,
                hover_name = "province_cap",
                color='midnight',
                center={"lat":50.87273172382932 , "lon": 4.590610254578612},
                mapbox_style="carto-positron",
                title="Average Intervention Duration",
                labels=labels_1,
                #    hover_data = hover_data,
                zoom=6.5)


                interventions_risk_line_period = interventions_risk_line[interventions_risk_line["time_period"]=="Midnight-Dawn {23.00-08.00}"].reset_index(drop=True)

                labels = {"Province intervention":"Province", "Intervention duration":"Intervention Duration"}

                fig_bar_dur = px.bar(interventions_risk_line_period, 
                    x='Province intervention', 
                    y='Intervention duration', 
                    color="Province intervention",
                    title="Average Intervention Duration - Midnight-Dawn {23.00-08.00}",
                    labels=labels)
        
    return fig_bar_dur, fig_intervention












