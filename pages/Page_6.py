import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output

dash.register_page(__name__,name="Emergency Assistance")


# Define the layout
layout = html.Div([
    html.H1('Emergency Assistance'),
    html.Button('HELP', id='help-button', n_clicks=0, style={'background-color': 'red', 'color': 'white', 'font-size': '24px', 'padding': '20px 40px', 'border-radius': '10px', 'cursor': 'pointer', 'margin': '50px auto', 'display': 'block'}),
    html.Div(id='help-message', style={'text-align': 'center', 'font-size': '18px', 'margin-top': '20px'}),
    dcc.Geolocation(id="geolocation"),
    html.Div(id="text_position",style={'text-align': 'center', 'font-size': '18px', 'margin-top': '20px'}),
    ],style={'background-color':'rgb(224, 255, 252)'})

# Define callback to show help message when button is clicked
@callback(
    Output("help-message", "children"),
    [Input("help-button", "n_clicks")]
)

def display_help_message(n_clicks):
    if n_clicks and n_clicks > 0:
        return "We are sending out your location to nearby AEDs."
    else:
        return ""

# Define callback to display position
@callback(
    Output("text_position", "children"),
    [Input("geolocation", "local_date"), Input("geolocation", "position")]
)
def display_output(date, pos):
    if pos:
        return html.P(
            f"Latitude: {pos['lat']}, Longitude: {pos['lon']}, date:{date}.",
        )
    return "Waiting for the location"


# # Register the 6th page with the layout and callback
# dash.register_page(__name__, name="Emergency Assistance", layout=layout)

# if __name__ == '__main__':
#     app.run_server(debug=True)
