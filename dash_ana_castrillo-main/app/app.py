import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import date,datetime,timedelta
from flask import Flask
from sqlalchemy import create_engine


# Load data
dialect="mysql+pymysql://sistemesbd:bigdata2223@192.168.193.133:3306/alumnes" #Aquest es el servido de clase i la BD
sqlEngine=create_engine(dialect)
dbConnection = sqlEngine.connect()
dffeb= pd.read_sql('futuros_ana_febrero', dbConnection) #Aqui va la vostra taula
df=pd.read_sql('futuros_ana', dbConnection)
dffeb['fecha']=pd.to_datetime(dffeb['fecha'])
df['fecha']=pd.to_datetime(df['fecha'])
df.set_index('fecha',inplace=True)
dffeb.set_index('fecha',inplace=True)
   


# Initialize the app
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.QUARTZ])
app.title = 'futuros_ana'
app.config.suppress_callback_exceptions = True



color_map = {
    "Feb/23": "#FF0000",
    "Mar/23": "#00FF00",
    "Apr/23": "#0000FF",
    "May/23": "#FFFFFF", 
    "Jun/23": "# 2E8B57",
    "Jul/23": "# FF1493",
    "Aug/23": "# DC143C",
    "Sep/23": "# 800080"
    
}
dffeb["color"] = dffeb["periodo"].map(color_map)
df["color"] = df["periodo"].map(color_map)



fig = go.Figure()

for period, color in color_map.items():
    df_period = df[df["periodo"] == period]
    fig.add_trace(go.Scatter(
        x=df_period.index, y=df_period["valor"],
        mode='markers', marker_color=color,
        name=period
    ))

fig.update_layout(legend=dict(
    yanchor="top", y=0.99, xanchor="left", x=0.01
))

grafica = dcc.Graph(id='grafica', figure=fig)


####
fig = go.Figure()

for period, color in color_map.items():
    dffeb_period = dffeb[dffeb["periodo"] == period]
    fig.add_trace(go.Scatter(
        x=dffeb_period.index, y=dffeb_period["valor"],
        mode='markers', marker_color=color,
        name=period
    ))

fig.update_layout(legend=dict(
    yanchor="top", y=0.99, xanchor="left", x=0.01))




grafica1=dcc.Graph(id='grafica1', figure = fig )


app.layout = dbc.Container([ 
  
     dbc.Row(dbc.Col(html.H2("Futuros"), width={'size': 12, 'offset': 0, 'order': 0}), style = {'textAlign': 'center', 'paddingBottom': '1%'}),
  
     dbc.Row([
                    dbc.Col(html.Div([grafica1]), width=6),
                    dbc.Col(html.Div([grafica]), width=6),
         
                ]),
     dbc.Row([
        dbc.Col(html.Div([dbc.Alert("Realizado por Ana Belén Castrillo")]),width=12)
    ])
 ])


















if __name__ == '__main__':
    app.run_server()