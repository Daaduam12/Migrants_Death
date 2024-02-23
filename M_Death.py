#!/usr/bin/env python
# coding: utf-8

# ## Load the necessary libraries

# In[2]:


import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
migrant_df = pd.read_csv("migrant_deaths.csv", delimiter=',')

app = dash.Dash()

# server = 'M_Death.server'
df = migrant_df.groupby(
    ["cause_of_death", "description", "location", "latitude", "longitude", "route (Frontex)", "Date-month", "Year"]
)[["dead_and_missing", "dead", "missing"]].sum().reset_index()# grouping the required columns to use
dead = migrant_df.groupby('Year')['dead'].sum().reset_index()
missing = migrant_df.groupby('Year')['missing'].sum().reset_index()

mapbox_access_token = open("my-mapbox-token.txt").read()

fig = go.Figure(go.Scattermapbox(
    lat=df['latitude'],
    lon=df['longitude'],
    customdata=df['dead_and_missing'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,  # Use 'dead_and_missing' for size
        color='#ff0000',
        opacity=0.5),
    text=df['route (Frontex)']
))

fig.update_layout(
    title='Total Confirmed Dead and Missing Migrants migrating to and in Europe from Year 2000 to 2016',
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=30,
            lon=0
        ),
        pitch=0,
        zoom=2,
        style='outdoors'
    )
)


app.layout = html.Div(children=[
    html.H1(children='THE MIGRANTS DEATH PROJECT',
            style={'color': '#80b1d3', 'textAlign': 'center', 'fontSize': '40px'}),  # Adjust fontSize as needed

    html.Img(
        src="https://upload.wikimedia.org/wikipedia/commons/e/eb/PR_Logo_GCM.png",
        className='three columns',
        style={
            'height': '25%',
            'width': '25%',
            'display': 'block',  # Make it a block-level element
            'margin': 'auto',    # Center horizontally
            'margin-top': 20,
            'margin-bottom': 20  # Adjust margin as needed
        }),

    html.Div(children='''Dash - A Web Application framework of Migrant Deaths enroute to and in Europe''',
             style={'textAlign': 'center', 'font-size': '20px', 'color': '#FF1493'}),  # Adjust fontSize as needed

    dcc.Graph(figure=fig),
    dcc.Graph(id='graph2',
              style={"width": "75%", "display": "inline-block"},
              figure=px.scatter(df,
                                x="Year",
                                y="dead_and_missing",
                                size="dead_and_missing",
                                size_max=30,
                                hover_name="location",
                                color="route (Frontex)",
                                marginal_y="violin",
                                marginal_x="histogram",
                                log_x=False,
                                labels={'dead_and_missing': 'Total Number of Dead and Missing Migrants'},
                                title="Total Confirmed Dead and Missing Migrants migrating to Europe from Year 2000 to 2016 by Route"
                                )
              ),
    dcc.Graph(id='graph3',
              figure=px.scatter(df,
                                x="Year",
                                y="dead_and_missing",
                                size="dead_and_missing", color="cause_of_death", hover_name='location',
                                labels={'dead_and_missing': 'Total Number of Dead and Missing Migrants'},
                                log_x=True,
                                range_y=[8, 60],
                                size_max=30,
                                title="Total Confirmed Dead and Missing Migrants migrating to and in Europe from Year 2000 to 2016 by Cause of Death at the exact latitude"
                                )
              )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=1378, debug=True)


# In[ ]:




