import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

dash.register_page(__name__,name="Signup Page")

layout = html.Div([
    html.H1("Signup Page"),
    html.P("By signing up at this page, you will receive text notifications when someone near you is suffering from cardiac arrest and there is an AED located near you."),
    html.Div([
        html.Label("First Name"),
        dcc.Input(id='first-name', type='text', placeholder='Enter your first name'),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Label("Last Name"),
        dcc.Input(id='last-name', type='text', placeholder='Enter your last name'),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Label("Phone Number"),
        dcc.Input(id='phone-number', type='text', placeholder='Enter your phone number'),
    ], style={'margin-bottom': '10px'}),
    html.Div([
        html.Label("Location"),
        dcc.Input(id='location', type='text', placeholder='Enter your location'),
    ], style={'margin-bottom': '10px'}),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-message', style={'margin-top': '20px', 'color': 'green'})
],style={'background-color':'rgb(224, 255, 252)'})

@callback(
    Output('output-message', 'children'),
    Input('submit-button', 'n_clicks'),
    State('first-name', 'value'),
    State('last-name', 'value'),
    State('phone-number', 'value'),
    State('location', 'value')
)
def update_output(n_clicks, first_name, last_name, phone_number, location):
    if n_clicks > 0:
        # Here you would typically handle the signup logic, e.g., save to a database
        return f"Thank you {first_name} {last_name} for signing up! You will receive notifications at {phone_number}. Your location is {location}."
    return ""
