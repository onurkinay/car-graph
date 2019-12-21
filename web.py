import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import time
from flask import Flask, jsonify, abort, make_response, request, url_for
speed=-100
seconds = 0
updating = True


#################
fig = make_subplots(
    rows=2, cols=2, shared_xaxes=True, vertical_spacing=0.11, print_grid=True
    , specs=[ [ {"colspan":2} ,{}], [{},{}]] , subplot_titles=("Konum", "", "Hız", "Ivme")  )

data = { 'x':[], 'y':[]}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "/assets/style.css"]
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.title = "Araba grafiği çizme uygulaması"

app.layout = html.Div(html.Div(
    [
        dbc.Row(dbc.Col(html.Iframe(src=app.get_asset_url("car.html"), width="100%", id="car4", height="100px",style={'border':'none', 'overflow':'hidden'}))),
        dbc.Row(
            [
dbc.Col([
                    dcc.Graph(id='car-gra', figure=fig),
                    dcc.Interval(id='refresh',interval=1000, n_intervals=0),
    ]),
            ])]))


@server.route('/get-hiz', methods=['GET'])
def on_message():  # GET POST
    global speed
    global updating
    global seconds
    getspeed = request.args.get('hiz')
    if getspeed.find(',') != -1:
        speedarray = getspeed.split(",")
        for i in speedarray:
            data['x'].append(seconds)
            seconds+=1
            data['y'].append(float(i))
        speed = -100
    elif getspeed == "-1000":
        data['x'] = []
        data['y'] = []
        speed = -100
    else:
        speed = float(request.args.get('hiz'))
    print(data)
    updating = True
    return "ok"


@server.route('/sifirla', methods=['GET'])
def sifirlama():
    global speed
    global updating
    global seconds
    data['x'] = []
    data['y'] = []
    seconds = 0
    updating = True
    return "ok"


@server.route('/durdur', methods=['GET'])
def durdur():
    global updating
    updating = False
    return "ok"


################
@app.callback(Output('car-gra', 'figure'),
              [Input('refresh', 'n_intervals')])
def update_graph_live(n):
    global speed
    global seconds
    global fig
    global updating
    if updating:
        updating = False
        if speed == -1000:
            return False
        if speed != -100:
            data['x'].append(seconds)
            data['y'].append(speed)
            seconds += 1

        dataAcc = {
                'x': [],
                'y': [0]
                }
        dataPlace = {
                'x': [],
                'y': [0]
                }
        for i in range(len((data['y']))):###SOME CALC.

            if data['x'][i] != 0:
                acc = (data['y'][i] - data['y'][i-1]) / (data['x'][i] - data['x'][i-1])
                dataAcc['x'] = data['x']
                dataAcc['y'].append(acc)

                place = dataPlace['y'][i-1] + (data['y'][i])
                dataPlace['x'] = data['x']
                dataPlace['y'].append(place)



        fig.data = []
        fig.add_trace(go.Scatter(x=data['x'], y=data['y'], name="hız"), row=2, col=1)
        fig.add_trace(go.Scatter(x=dataAcc['x'], y=dataAcc['y'], name="ivme", line_shape='vh'), row=2, col=2)
        fig.add_trace(go.Scatter(x=dataPlace['x'],y=dataPlace['y'], name="konum", line_shape='spline'),row=1, col=1)
        fig.update_layout(margin=dict(l=0, r=0, t=35, b=10), height=650)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8000)

