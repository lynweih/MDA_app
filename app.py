import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)
server=app.server

app.layout = html.Div([
    html.H1("Exploration & Analysis of AED Locations in Relation to Emergency Services and Cardiac Arrests in Belgium"
            ,style={'text-align':'center'}),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
































