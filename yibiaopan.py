#!/usr/bin/env python3
#coding=utf-8

import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

import rospy
from geometry_msgs.msg import TwistStamped
import numpy as np

mav_speed = 0.
max_speed = 0.

fig = go.Figure()
fig.add_trace(go.Indicator(
    name = "my_trace",
    domain={'x': [0, 1], 'y': [0, 1]},
    value=450.00,
    mode="gauge+number",
    title={'text': "Speed [m/s]", 'font': {'size': 28}},
    gauge={
        #    'axis': {'range': [None, 25]},
        #    'steps': [
        #        {'range': [0, 12.5], 'color': "lightgray"},
        #        {'range': [12.5, 20], 'color': "darkgray"},
        #        {'range': [20, 25], 'color': "gray"}],
           'axis': {'range': [None, 12]},
           'steps': [
               {'range': [0, 6], 'color': "lightgray"},
               {'range': [6, 9], 'color': "darkgray"},
               {'range': [9, 12], 'color': "gray"}],
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 25}}
    # gauge={'axis': {'range': [None, 20]},
    #        'bar': {'color': "blue"},
    #        'steps': [
    #            {'range': [0, 10], 'color': "green"},
    #            {'range': [10, 15], 'color': "yellow"},
    #            {'range': [15, 20], 'color': "red"}],
    #        'threshold': {'line': {'color': "darkred", 'width': 4}, 'thickness': 0.75, 'value': 19}}
))
fig.update_layout(font = {'size': 20})

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig,id="my_gauge"),
    # timing trigger
    dcc.Interval(
            id='time',
            interval=33, # in milliseconds
            n_intervals=0)
])


@app.callback(
    Output('my_gauge', 'figure'),
    Input(component_id = 'time', component_property='n_intervals')
    )
def update_gauge(value):
    global mav_speed, max_speed
    fig.update_traces(value=mav_speed, selector=dict(name="my_trace"))
    # fig.update_traces(value=mav_speed, selector=dict(name="my_trace"), gauge={'threshold': {'value': max_speed}})
    return fig

def mav_vel_cb(msg):
    global mav_speed, max_speed
    mav_speed = np.linalg.norm([msg.twist.linear.x, msg.twist.linear.y, msg.twist.linear.z])
    if mav_speed > max_speed: max_speed = mav_speed
    # print(mav_speed)

if __name__ == "__main__":
    rospy.init_node('offb_node', anonymous=True)
    rospy.Subscriber("mavros/local_position/velocity_local", TwistStamped, mav_vel_cb)

    app.run_server(debug=True)
    rospy.spin()
