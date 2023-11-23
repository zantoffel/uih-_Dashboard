import dash
from dash import html
from dash import dcc
import figs


app = dash.Dash(__name__)
run = app.server                        # cmd: gunicorn -w 4 Dashboard:run        to run server using green unicorn (dedizierter WSGI (Web Server Gateway Interface))

map_figs = figs.get_figs("DB")
maps_fig = map_figs[0]
heat_fig = map_figs[1]
wetter_figs = figs.get_wetter_figs()
temp_fig = wetter_figs[0]
rain_fig = wetter_figs[1]
wind_fig = wetter_figs[2]


# Layout der Dash-Anwendung festlegen
config_graph= {'displayModeBar': False}

app.layout = html.Div([
    html.Div([
    dcc.Graph(id='temp-graph', figure=temp_fig, config=config_graph, style={'width': '90%', 'height': '30vh'}),
    dcc.Graph(id='rain-graph', figure=rain_fig, config=config_graph, style={'width': '90%', 'height': '30vh'}),
    dcc.Graph(id='wind-graph', figure=wind_fig, config=config_graph, style={'width': '90%', 'height': '30vh'}),
    ], style={'width': '28%', 'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'background-color': 'rgb(17,17,17)', 'border-radius': '15px', 'height': '95vh'}),
    
    html.Div([
    dcc.Dropdown(
    id='data-source-dropdown',
    options=[
        {'label': 'ÖPNV', 'value': 'DB'},
        {'label': 'Essen', 'value': 'essen'},
        {'label': 'Tanken', 'value': 'tanken'},
        {'label': 'Parken', 'value': 'parken'},
        {'label': 'Einzelhandel', 'value': 'einzelhandel'},
        {'label': 'Dienstleistungsgeschäfte', 'value': 'dienstleistungsgeschäfte'}
    ],
    value='essen',  # Default selected value
    style={'width': '95%', 'margin-top': '1em'}#, 'height': '10vh'
),
    dcc.Graph(id='mainMap', figure=maps_fig, style={'width': '50%', 'height': '65vh'}, config=config_graph),
    dcc.Graph(id='heatMap', figure=heat_fig, style={'width': '50%', 'height': '65vh'}, config=config_graph),
    dcc.Textarea(id='infoText', value='', style={'width': '95%', 'padding': '10px', 'margin': '1em 0', 'border-radius': '10px', 'background-color': 'rgb(88,98,222)'}),
    ], style={'width': '60%', 'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'background-color': 'rgb(17,17,17)', 'margin': '0 2em', 'border-radius': '15px', 'height': '95vh'})
],style={'display': 'flex', 'flex-wrap': 'wrap', 'background-color': 'rgb(48,48,48)', 'padding': '10px', 'height': '96vh', 'border-radius': '20px'})

# Callback to update map based on dropdown selection
@app.callback(
    [dash.dependencies.Output('mainMap', 'figure'),
     dash.dependencies.Output('heatMap', 'figure')],
    [dash.dependencies.Input('data-source-dropdown', 'value')]
)

def update_map(selected_data_source):
    map_figs = figs.get_figs(selected_data_source)
    maps_fig = map_figs[0]
    heat_fig = map_figs[1]
    return maps_fig, heat_fig

#Clickable points
@app.callback(
dash.dependencies.Output('infoText', 'value'),
[dash.dependencies.Input('mainMap', 'clickData')]
)

def display_click_data(clickData):
    if clickData is not None:
    # Extract information from clickData and update the output box
        clicked_text = clickData['points'][0]['customdata']
        return "You clicked on: {\'name\': \'"+str(clicked_text[0])+"\', \'location\': \'{\'latitude\': \'"+str(clicked_text[1])+"\', \'longitude\': \'"+str(clicked_text[2])+"\'}, \'icon\': \'"+str(clicked_text[3])+"\', \'accessibilityOptions\': \'"+str(clicked_text[4])+"\'}"
    else:
        return 'Click on a marker to see more information'

#Start app
    
        

if __name__ == "__main__":
    app.run_server(debug=False)

'''
priceLevel, places.accessibilityOptions, rating, places.restroom, places.servesBeer
'''