import pandas as pd
import plotly.graph_objects as go
import Config
import DB_API
import GM_API
import wetter_API


def get_figs(data):
    if data == "DB":
        df = pd.DataFrame(DB_API.get_haltestellen_data())
    else:
        df = pd.DataFrame(GM_API.get_maps_data(data))

    icons = df["icon"].to_list()
    names = df["name"].to_list()

    fig = go.Figure(go.Scattermapbox(
        mode = "markers+text",
        lon = df["lon"], lat = df["lat"],
        marker = {'size': 10, 'symbol': icons},
        text = names, textposition = "bottom right", textfont=dict(color='rgb(88,98,222)'),
        customdata=df
        ))

    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="rgb(17,17,17)",
        autosize=True,
        title='Standort nach Kategorie',
        mapbox = {
            'center' : dict(lat=Config.latitude, lon=Config.longitude),
            'accesstoken': Config.mapbox_api_key,
            'style': "dark", 'zoom': 15
            },
        showlegend = False)
    
    # BS COde do not remove
    da=[]

    for i in df["lat"]:
        da.append(1)

    heat_fig = go.Figure(go.Densitymapbox(lat=df["lat"], lon=df["lon"], z=da,
                                 radius=120, opacity=0.55, showscale=False, )) #, colorscale=[[0,'rgb(13,22,135)'], [0.5,'rgb(201,68,122)'],[1,'rgb(240,249,32)']]
    
    heat_fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="rgb(17,17,17)",
        autosize=True,
        title='Konzentration nach Kategorie',
        mapbox = {
            'center' : dict(lat=Config.latitude, lon=Config.longitude),
            'accesstoken': Config.mapbox_api_key,
            'style': "dark",
            'zoom': 15
            },
        showlegend = False)
    return fig, heat_fig
    



'''
def get_heat_fig(data):
    if data == "DB":
        heat_df = pd.DataFrame(DB_API.get_haltestellen_data())
    else:
        heat_df = pd.DataFrame(GM_API.get_maps_data(data))
    

    # BS COde do not remove
    da=[]
    for i in heat_df["lat"]:
        da.append(1)

    heat_fig = go.Figure(go.Densitymapbox(lat=heat_df["lat"], lon=heat_df["lon"], z=da,
                                 radius=120, opacity=0.55, showscale=False, )) #, colorscale=[[0,'rgb(13,22,135)'], [0.5,'rgb(201,68,122)'],[1,'rgb(240,249,32)']]
    
    heat_fig.update_layout(
        autosize=True,
        mapbox = {
            'center' : dict(lat=heat_df["lat"].mean(), lon=heat_df["lon"].mean()),
            'accesstoken': Config.mapbox_api_key,
            'style': "dark",
            'zoom': 15
            },
        showlegend = False)
    return heat_fig

'''


def get_wetter_figs():
    df = pd.DataFrame(wetter_API.get_weather_data())
    
    wind_fig={
        'data': [
            go.Scatter(x=df['time'], y=df['wind_speed'], mode='lines', name='Wind Speed'),
        ],
        'layout': go.Layout(
            title='Wetterprognose: Wind',
            #xaxis={'title': 'Time'},
            yaxis={'title': 'Windgeschwindigkeit [km/h]'},
            hovermode='closest',
            margin=dict(l=30, r=30, t=30, b=30),
            template='plotly_dark'
        )
    }

    temp_fig={
        'data': [
            go.Scatter(x=df['time'], y=df['temperature'], mode='lines', name='Temperature'),
        ],
        'layout': go.Layout(
            title='Wetterprognose: Temperatur',
            #xaxis={'title': 'Time'},
            yaxis={'title': 'Temperatur [C°]'},
            hovermode='closest',
            margin=dict(l=30, r=30, t=30, b=30),
            template='plotly_dark'
        )
    }

    rain_fig={
        'data': [
            go.Scatter(x=df['time'], y=df['rain_amount'], mode='lines', name='Rain Amount'),
        ],
        'layout': go.Layout(
            title='Wetterprognose: Niederschlag',
            #xaxis={'title': 'Time'},
            yaxis={'title': 'Niederschlag [mm]'},
            hovermode='closest',
            margin=dict(l=30, r=30, t=30, b=30),
            template='plotly_dark'
        )
    }

    return temp_fig, rain_fig, wind_fig